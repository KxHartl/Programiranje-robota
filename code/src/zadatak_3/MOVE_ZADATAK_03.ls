/PROG  MOVE_ZADATAK_03
/ATTR
OWNER		= MNEDITOR;
COMMENT		= "Z3 Busenje";
PROG_SIZE	= 550;
CREATE		= DATE 26-02-12  TIME 14:00:00;
MODIFIED	= DATE 26-02-12  TIME 14:00:00;
FILE_NAME	= ;
VERSION		= 0;
LINE_COUNT	= 9;
MEMORY_SIZE	= 950;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/APPL
/MN
   1:  UFRAME_NUM=0 ;
   2:  UTOOL_NUM=0 ;
   3:  !Pomak iznad tocke busenja ;
   4:  J PR[10:Iznad] 100% FINE    ;
   5:  !Spustanje na poziciju busenja ;
   6:  L PR[11:Busenje] R[10:Brzina]mm/sec FINE    ;
   7:  !Povratak prema gore ;
   8:  L PR[10:Iznad] 200mm/sec FINE    ;
   9:  !Kraj programa ;
/POS
/END
