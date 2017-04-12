//------------------------------------------------------------------------------
// main.cpp - функция, тестирующая работу сканера
//------------------------------------------------------------------------------

#include     <string.h>
#include     <stdio.h>

#include     "scaner_ext.h"

//------------------------------------------------------------------------------

void fprintlex(FILE*);   // тестовый вывод результатов работы сканера
bool scan_init(char*);   // начальная установка сканера (нужна только здесь)
void scan_destroy(void); // завершение работы сканера

//------------------------------------------------------------------------------

FILE    *outfil;

void main(int argc, char** argv)
{
  if(argc != 3) {
    printf("\nIncorrect command format!\n");
    printf("\nYou must type: command sourced_file recived_file.\n");
    return;
  }

  outfil = fopen(argv[2], "w");
  line = 1; column = 0;

  if(!scan_init(argv[1])) return;
  
  while(lc != lexEof) 
  {
    nxl(); fprintlex(outfil);
  }
  
  printf("\nEnd of scaning!\n");

  scan_destroy();
  fclose(outfil);
} 

//------------------------------------------------------------------------------

