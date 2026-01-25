"""
Robot Movement Analysis - Tool Tracking and Motion Comparison
Compares linear (MoveL), joint (MoveJ), and circular (MoveC) motions
Records and visualizes tool position, joint angles, velocities, and accelerations
"""

from robodk.robolink import *
from robodk.robomath import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
from pathlib import Path
import traceback

# ========== CONFIGURATION AND INITIALIZATION ==========

# Initialize RoboDK connection and set execution mode
rdk = Robolink()
rdk.setRunMode(1)

# Determine output directory for generated graphs
output_dir = Path("outputs/zadatak_01")
output_dir.mkdir(parents=True, exist_ok=True)

# Retrieve robot, target points, and tool for tracking
robot = rdk.Item('', ITEM_TYPE_ROBOT)
target_1 = rdk.Item('Point_1')
target_2 = rdk.Item('Point_2')
target_3 = rdk.Item('Mid_Point')
tool_tracked = rdk.Item('Tool 1', ITEM_TYPE_TOOL)

# Validate all required items exist in the station
if not all([robot.Valid(), target_1.Valid(), target_2.Valid(), target_3.Valid(), tool_tracked.Valid()]):
    print("Error: Robot, target points (Point_1, Point_2, Mid_Point), or tool 'Tool 1' not found!")
    exit()

# Data storage structure for each motion type
motion_data = {
    'MoveL': {'time': [], 'position': [], 'joints': []},
    'MoveJ': {'time': [], 'position': [], 'joints': []},
    'MoveC': {'time': [], 'position': [], 'joints': []}
}

# ========== DATA RECORDING AND PROCESSING ==========

def execute_and_record_motion(motion_type):
    """
    Execute a single motion experiment: position robot at initial point,
    record tool position and joint angles during motion, store collected data.
    
    Args:
        motion_type (str): Type of motion ('MoveL', 'MoveJ', or 'MoveC')
    """
    # Move to initial position
    robot.MoveJ(target_1, blocking=True)
    time.sleep(0.1)

    # Initialize timing and data collection
    start_time = time.time()
    temp_data = {'time': [], 'position': [], 'joints': []}
    
    # Define motion commands for each type
    motion_commands = {
        'MoveL': (robot.MoveL, target_2),
        'MoveJ': (robot.MoveJ, target_2),
        'MoveC': (robot.MoveC, target_3, target_2)
    }

    # Execute non-blocking motion command
    motion_func, *motion_args = motion_commands[motion_type]
    motion_func(*motion_args, blocking=False)

    # Collect data while robot is moving
    while robot.Busy():
        # Record elapsed time
        temp_data['time'].append(time.time() - start_time)
        
        # Get tool tip position: flange pose × tool offset = world position
        flange_pose = robot.Pose()
        tool_world_position = flange_pose * tool_tracked.Pose()
        temp_data['position'].append(Pose_2_TxyzRxyz(tool_world_position))
        
        # Record all six joint angles
        joint_angles = robot.Joints()
        temp_data['joints'].append(
            joint_angles.tolist() if hasattr(joint_angles, 'tolist') 
            else [angle[0] for angle in joint_angles]
        )
        time.sleep(0.01)

    # Store processed data for later analysis
    for key, value in temp_data.items():
        motion_data[motion_type][key] = np.array(value) if value else np.array([])


def resample_and_process_data(target_points=300):
    """
    Process raw motion data: normalize all motions to common time axis (resampling),
    compute derivatives for smooth velocity and acceleration profiles.
    
    Args:
        target_points (int): Number of points for interpolation
        
    Returns:
        dict: Processed motion data with interpolated values and derivatives
    """
    # Find maximum motion duration to establish common time axis
    durations = [
        data['time'][-1] for data in motion_data.values() 
        if len(data['time']) > 0
    ]
    if not durations:
        return None
    
    max_duration = max(durations)
    time_axis = np.linspace(0, max_duration, target_points)
    processed_results = {}

    for motion_type, raw_data in motion_data.items():
        # Skip if insufficient data points
        if len(raw_data['time']) < 2:
            continue
        
        # Interpolate position and joint data onto common time axis
        interpolated_positions = np.array([
            np.interp(time_axis, raw_data['time'], raw_data['position'][:, i]) 
            for i in range(6)
        ]).T
        
        interpolated_joints = np.array([
            np.interp(time_axis, raw_data['time'], raw_data['joints'][:, i]) 
            for i in range(6)
        ]).T
        
        # Compute first and second derivatives from interpolated data
        velocity = np.gradient(interpolated_joints, time_axis, axis=0)
        acceleration = np.gradient(velocity, time_axis, axis=0)
        
        processed_results[motion_type] = {
            'time': time_axis,
            'position': interpolated_positions,
            'joints': interpolated_joints,
            'velocity': velocity,
            'acceleration': acceleration
        }
    
    return processed_results


# ========== GRAPH GENERATION AND VISUALIZATION ==========

def generate_comparison_plots(processed_data):
    """
    Create four publication-quality comparison figures showing motion profiles.
    Each figure contains six subplots (one per degree of freedom).
    
    Args:
        processed_data (dict): Processed motion data from resample_and_process_data()
    """
    if not processed_data:
        return

    # Define visual styles for each motion type
    style_config = {
        'MoveL': {'color': "#6200ff", 'linestyle': '-', 'label': 'Linear Motion', 'linewidth': 1},
        'MoveJ': {'color': "#09ff00", 'linestyle': '-', 'label': 'Joint Motion', 'linewidth': 1},
        'MoveC': {'color': "#ff0000", 'linestyle': '-', 'label': 'Circular Motion', 'linewidth': 1}
    }
    
    # Define data types to plot with their properties
    plot_specifications = {
        'Tool Position x(t)': {
            'data_key': 'position',
            'filename': '01_Tool_Position.png',
            'axis_labels': ['x(t) [mm]', 'y(t) [mm]', 'z(t) [mm]', 
                           'rx(t) [°]', 'ry(t) [°]', 'rz(t) [°]']
        },
        'Joint Angles q(t)': {
            'data_key': 'joints',
            'filename': '02_Joint_Angles.png',
            'axis_labels': [f'q{i+1}(t) [°]' for i in range(6)]
        },
        'Joint Velocities q̇(t)': {
            'data_key': 'velocity',
            'filename': '03_Joint_Velocities.png',
            'axis_labels': [f'q̇{i+1}(t) [°/s]' for i in range(6)]
        },
        'Joint Accelerations q̈(t)': {
            'data_key': 'acceleration',
            'filename': '04_Joint_Accelerations.png',
            'axis_labels': [f'q̈{i+1}(t) [°/s²]' for i in range(6)]
        }
    }

    # Generate each comparison figure
    for plot_title, plot_config in plot_specifications.items():
        fig = plt.figure(figsize=(18, 10))
        fig.suptitle(f'Task 1: Motion Comparison - {plot_title}', 
                    fontsize=20, fontweight='bold', y=0.995)
        
        # Create 2×3 subplot grid
        gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)
        
        # Plot data for each degree of freedom
        for dof_index, ax in enumerate([fig.add_subplot(gs[i, j]) 
                                        for i in range(2) for j in range(3)]):
            # Plot each motion type
            for motion_type, style in style_config.items():
                data_array = processed_data[motion_type][plot_config['data_key']]
                
                if data_array.shape[1] > dof_index:
                    ax.plot(processed_data[motion_type]['time'], 
                           data_array[:, dof_index],
                           color=style['color'],
                           linestyle=style['linestyle'],
                           label=style['label'],
                           linewidth=style['linewidth'],
                           alpha=0.85)
            
            # Configure subplot appearance
            ax.set_title(plot_config['axis_labels'][dof_index], 
                        fontsize=13, fontweight='bold')
            ax.set_xlabel('Time [s]', fontsize=11)
            ax.set_ylabel(plot_config['axis_labels'][dof_index], fontsize=11)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_axisbelow(True)
        
        # Add unified legend below plots
        handles = [plt.Line2D([0], [0], **style) for style in style_config.values()]
        fig.legend(handles=handles, loc='lower center', ncol=3, 
                  fontsize=12, frameon=True, fancybox=True, shadow=True, 
                  bbox_to_anchor=(0.5, -0.02))
        
        # Save figure with high resolution
        output_path = output_dir / plot_config['filename']
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {plot_config['filename']}")
        plt.close(fig)


# ========== MAIN EXECUTION BLOCK ==========

if __name__ == "__main__":
    try:
        print(f"Output directory: {output_dir}")
        print("Configuring robot parameters...")
        
        # Set robot motion parameters
        robot.setSpeed(100)
        robot.setAcceleration(100)

        print("Starting motion experiments...")
        
        # Execute all three motion types and collect data
        for motion_type in motion_data.keys():
            print(f"  Recording {motion_type} motion...")
            execute_and_record_motion(motion_type)
            print(f"  ✓ {motion_type} complete")

        print("Processing collected data...")
        
        # Resample and compute derivatives
        final_processed_data = resample_and_process_data()
        
        print("Generating comparison plots...")
        
        # Create visualization figures
        generate_comparison_plots(final_processed_data)
        
        print("\n" + "="*50)
        print("Analysis completed successfully!")
        print(f"Results saved to: {output_dir}")
        print("="*50)

    except Exception as error:
        print(f"\nCRITICAL ERROR: {error}")
        traceback.print_exc()
