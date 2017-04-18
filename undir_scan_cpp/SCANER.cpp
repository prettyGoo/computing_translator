//------------------------------------------------------------------------------
// saner.cpp - модуль лексического анализатора
//------------------------------------------------------------------------------

#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "scaner_data.h"
#include "scaner_local.h"

//------------------------------------------------------------------------------

void er(int i); // Импорт интерфейса функции вывода ошибок

//------------------------------------------------------------------------------
// Функции транслитератора, используемые для определения класса лексем
//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу букв
bool inline isLetter(int ch) {
  if((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z'))
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу двоичных цифр
bool inline isBin(int ch) {
  if((ch == '0' || ch == '1'))
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу восьмиричных цифр
bool inline isOctal(int ch) {
  if((ch >= '0' && ch <= '7'))
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу десятичных цифр
bool inline isDigit(int ch) {
  if((ch >= '0' && ch <= '9'))
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу шестнадцатиричных цифр
bool inline isHex(int ch) {
  if((ch >= '0' && ch <= '9') ||
     (ch >= 'A' && ch <= 'F') || 
     (ch >= 'a' && ch <= 'f'))
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу пробелов
bool inline isSkip(int ch) {
  if(ch == ' ' || ch == '\t' || ch == '\n' || ch == '\f')
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Определяет принадлежность символа к классу игнорируемых
bool inline isIgnore(int ch) {
  if(ch >0 && ch < ' ' && ch != '\t' && ch != '\n' && ch != '\f')
    return true;
  else
    return false;
}

//------------------------------------------------------------------------------

// Читает следующий символ из входного потока
static void nxsi(void)
{
    if((si = getc(infil)) == '\n') {++line; column = 0;}
    else ++column;
    ++poz; // Переход к следующей позиции в файле
}

//------------------------------------------------------------------------------

// откат назад при неудачной попытке распознать лексему
static void unset() {
  fseek(infil, oldpoz, 0);  
  nxsi();
  i_lv=-1; 
  lv[0]='\0'; 
  poz = oldpoz;
  line=oldline; 
  column=oldcolumn;
}

//------------------------------------------------------------------------------

// Определяет принадлежность к ключевому слову
static void find_idkw(void)
{
  for(int i = 0; i < rw_size; ++i)
    if(!strcmp(rwtab[i].wrd, lv)) {
      lc = rwtab[i].lc;
      return;
    }
  lc = lexId;
}

//------------------------------------------------------------------------------

// Распознавание идентификатора или ключевого слова
static bool id_etc()
{
    if(isLetter(si) || si == '_') {
      lv[++i_lv]=si; nxsi();
    }
    else 
      return false;

    while(isLetter(si) || isDigit(si) || si=='_') {
        lv[++i_lv] = si;
        nxsi();
    }
    lv[++i_lv] = '\0';
    find_idkw(); 
    return true;
}

//------------------------------------------------------------------------------

// Строка символов
static bool string_const(void)
{
//_0:
  if(si == '\"') { // начало строки
    nxsi(); goto _1;
  }
  else 
    return false;
_1:
  if(si == '\"') { // пустиая строка или апостроф в строке
    nxsi(); goto _2;
  }
  if(si == EOF) { // конец файла, а строка не закончилась
    lc = lexError; 
    lv[++i_lv]='\0'; 
    er(6); 
    return true; //  чтобы не было отката
  } 
  lv[++i_lv]=si; 
  nxsi();
  goto _1; // любой другой символ внутри строки
_2:
  if(si == '\"') { // дубль для апострофа
    lv[++i_lv]=si; // фиксируем его в строке как один     
    nxsi(); 
    goto _1;
  }
  lc = lexString; lv[++i_lv] = '\0'; return true; // законченная строка
}

//------------------------------------------------------------------------------

// Распознавание комментария
static bool comment()
{
    if(si=='/') {nxsi();}
    else return false;
    if(si != '*') {return false;}
    nxsi();
    loop:if(si == EOF) {lc = lexError; lv[++i_lv]='\0'; er(2); return true;} 
    while(si != '*') {
        lv[++i_lv] = si;
        if(si == EOF) {lc = lexError; lv[++i_lv]='\0'; er(2); return true;} 
        nxsi();
    }
    nxsi(); if(si != '/') {lv[++i_lv] = si; goto loop;}
    lv[++i_lv] = '\0';
    lc = lexComment;
    nxsi();
    return true;   
}

//------------------------------------------------------------------------------

// Распознавание целого десятичного числа
static bool decimal() {
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexInt; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание целого десятичного числа с префиксом
static bool pdecimal() {
  if(si=='{') nxsi(); else return false;
  if(si=='1'){lv[++i_lv]='1'; nxsi();} else return false;
  if(si=='0'){lv[++i_lv]='0'; nxsi();} else return false;
  if(si=='}'){lv[++i_lv]='#'; nxsi();} else return false;
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexInt; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание целого двоичного числа
static bool binary() {
  if(si=='{') nxsi(); else return false;
  if(si=='2'){lv[++i_lv]='1'; nxsi();} else return false;
  if(si=='}'){lv[++i_lv]='#'; nxsi();} else return false;
  if(si=='0'||si=='1'){lv[++i_lv]=si; nxsi();} else return false;
  while (si=='0'||si=='1'){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexInt; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание целого восьмиричного числа
static bool octal() {
  if(si=='{') nxsi(); else return false;
  if(si=='8'){lv[++i_lv]='8'; nxsi();} else return false;
  if(si=='}'){lv[++i_lv]='#'; nxsi();} else return false;
  if(si>='0' && si<='7'){lv[++i_lv]=si; nxsi();} else return false;
  while (si>='0' && si<='7') {
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexInt; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание целого шестнадцатиричного числа
static bool hex() {
  if(si=='{') nxsi(); else return false;
  if(si=='1'){lv[++i_lv]='1'; nxsi();} else return false;
  if(si=='6'){lv[++i_lv]='0'; nxsi();} else return false;
  if(si=='}'){lv[++i_lv]='#'; nxsi();} else return false;
  if(isHex(si)) {
    lv[++i_lv]=si; nxsi();
  } 
  else return false;
  while (isHex(si)) {
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexInt; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание первой версии дейстительного числа
static bool float1() {
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(si=='e'||si=='E') {lv[++i_lv]=si; nxsi();} else return false;
  if(si=='+'||si=='-') {lv[++i_lv]=si; nxsi();} 
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexFloat; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание второй версии дейстительного числа
static bool float2() {
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(si=='.') {lv[++i_lv]=si; nxsi();} else return false;
  while(isDigit(si)) {lv[++i_lv]=si; nxsi();}
  if(si=='e'||si=='E') {lv[++i_lv]=si; nxsi();} else return false;
  if(si=='+'||si=='-') {lv[++i_lv]=si; nxsi();} 
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexFloat; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание третьей версии дейстительного числа
static bool float3() {
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(si=='.') {lv[++i_lv]=si; nxsi();} else return false;
  while(isDigit(si)) {lv[++i_lv]=si; nxsi();}
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexFloat; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание четвертой версии дейстительного числа
static bool float4() {
  if(si=='.') {lv[++i_lv]=si; nxsi();} else return false;
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(si=='e'||si=='E') {lv[++i_lv]=si; nxsi();} else return false;
  if(si=='+'||si=='-') {lv[++i_lv]=si; nxsi();} 
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexFloat; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------

// Распознавание пятой версии дейстительного числа
static bool float5() {
  if(si=='.') {lv[++i_lv]=si; nxsi();} else return false;
  if(isDigit(si)){lv[++i_lv]=si; nxsi();} else return false;
  while (isDigit(si)){
    lv[++i_lv] = si;
    nxsi();
  }
  if(isLetter(si)) {lc=lexError; lv[++i_lv]='\0'; er(3); return true;}
  lc = lexFloat; lv[++i_lv] = '\0'; return true; 
}

//------------------------------------------------------------------------------
// Функция, формирующая следующую лексему
// Вызывается синтаксическим анализатором
//------------------------------------------------------------------------------

void nxl(void) {
  do {
    i_lv = -1;   
    lv[0] = '\0';

    // Фиксируем начальную позицию
    oldpoz=ftell(infil)-1;
    oldline=line; oldcolumn=column;

    // Процесс пошел
    if(si == EOF) {lc = lexEof; return;}
    // Игнорируемую лексему не возвращаем
    if(isSkip(si)) {nxsi(); lc = lexSkip; continue; /*return;*/}
    if(id_etc())       {return;} unset();
    if(string_const()) {return;} unset();
    if(float1())       {return;} unset();
    if(float2())       {return;} unset();
    if(float3())       {return;} unset();
    if(float4())       {return;} unset();
    if(float5())       {return;} unset();
    if(binary())       {return;} unset();
    if(octal())        {return;} unset();
    if(hex())          {return;} unset();
    if(pdecimal())     {return;} unset();
    if(decimal())      {return;} unset();
    // Игнорируемую лексему не возвращаем
    if(comment())      {continue; /*return;*/} unset();
    // Игнорируемую лексему не возвращаем
    if(isIgnore(si)) {nxsi(); lc = lexIgnore; continue; /*return;*/}
    if(si=='/') {nxsi(); lc = lexSlash;return;}
    if(si == ';') {nxsi(); lc = lexSemicolon; return;}
    if(si == ',') {nxsi(); lc = lexComma; return;}
    if(si == ':') {
      nxsi(); 
      if(si == '=') {nxsi(); lc = lexAssign; return;}
    } unset();
    if(si==':') {nxsi(); lc = lexColon; return;}
    if(si == '(') {nxsi(); lc = lexLftRndBr; return;}
    if(si == ')') {nxsi(); lc = lexRghRndBr; return;}
    if(si == '[') {nxsi(); lc = lexLftSqBr; return;}
    if(si == ']') {nxsi(); lc = lexRghSqBr; return;}
    if(si == '*') {nxsi(); lc = lexStar; return;}
    if(si == '%') {nxsi(); lc = lexPercent; return;}
    if(si == '+') {nxsi(); lc = lexPlus; return;}
    if(si == '-') {
      nxsi(); 
      if(si == '>') {nxsi(); lc = lexArrow; return;}  
    } unset();
    if(si=='-') {nxsi(); lc=lexMinus; return;}
    if(si == '=') {nxsi(); lc = lexEQ; return;}
    if(si == '!') {
      nxsi(); 
      if(si == '=') {nxsi(); lc = lexNE; return;}
    } unset();
    if(si == '>') {
      nxsi(); 
      if(si == '=') {nxsi(); lc = lexGE; return;}
    } unset();
    if(si=='>') {nxsi(); lc=lexGT; return;}
    if(si == '<') {
      nxsi(); 
      if(si == '=') {nxsi(); lc = lexLE; return;}
    } unset();
    if(si=='<') {nxsi(); lc=lexLT; return;}
    lc = lexError; er(0); nxsi();
  } while (lc == lexComment || lc == lexSkip || lc == lexIgnore);
}

//------------------------------------------------------------------------------
// Функция, инициирующая работу со сканером
// Вызывается перед запуском синтаксического анализатора
//------------------------------------------------------------------------------

bool scan_init(char *file_name) {
  if((infil = fopen(file_name, "r"))==0) {
    printf("\nInput file is absent!\n"); return false;
  }

  nxsi();
  nxl();

  return true;
}

//------------------------------------------------------------------------------
// Функция, завершающая работу сканера
//------------------------------------------------------------------------------

void scan_destroy() {
  fclose(infil);
}
