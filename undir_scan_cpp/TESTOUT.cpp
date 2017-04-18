//------------------------------------------------------------------------------
// tesout.cpp - тестовый вывод информации о лексемах
//------------------------------------------------------------------------------

#include <stdio.h>
#include "scaner_ext.h"

//------------------------------------------------------------------------------

void fprintlex(FILE* f) 
{
  char* lcs;
  char* lvs;
  switch(lc) 
  {
    case lexPlus:       lcs="lexPlus";      lvs="+";  break;
    case lexAssign:     lcs="lexAssign";    lvs=":="; break;
    case lexComma:      lcs="lexComma";     lvs=",";  break;
    case lexComment:    lcs="lexComment";   lvs=lv;   break;
    case lexSlash:      lcs="lexSlash";     lvs="/";  break;
    case lexColon:      lcs="lexColon";     lvs=":";  break;
    case lexEQ:         lcs="lexEQ";        lvs="=";  break;
    case lexEof:        lcs="lexEof";       lvs="-1"; break;
    case lexError:      lcs="lexError";     lvs=lv;   break;
    case lexFloat:      lcs="lexFloat";     lvs=lv;   break;
    case lexGE:         lcs="lexGE";        lvs=">="; break;
    case lexGT:         lcs="lexGT";        lvs=">";  break;
    case lexId:         lcs="lexId";        lvs=lv;   break;
    case lexIgnore:     lcs="lexIgnore";    lvs=lv;   break;
    case lexInt:        lcs="lexInt";       lvs=lv;   break;
    case lexLE:         lcs="lexLE";        lvs="<="; break;
    case lexLftRndBr:   lcs="lexLftRndBr";  lvs="(";  break;
    case lexLftSqBr:    lcs="lexLftSqBr";   lvs="[";  break;
    case lexLT:         lcs="lexLT";        lvs="<";  break;
    case lexPercent:    lcs="lexPercent";   lvs="%";  break;
    case lexStar:       lcs="lexStar";      lvs="*";  break;
    case lexString:     lcs="lexString";    lvs=lv;   break;
    case lexNE:         lcs="lexNE";        lvs="!="; break;
    case lexSemicolon:  lcs="lexSemicolon"; lvs=";";  break;
    case lexRghRndBr:   lcs="lexRghRndBr";  lvs=")";  break;
    case lexRghSqBr:    lcs="lexRghSqBr";   lvs="]";  break;
    case lexSkip:       lcs="lexSkip";      lvs=" ";  break;
    case lexArrow:      lcs="lexArrow";     lvs="->"; break;
    case lexMinus:      lcs="lexMinus";     lvs="-";  break;

    case kwAbort: lcs="KWABORT";  lvs=lv;   break;
    case kwBegin: lcs="KWBEGIN";  lvs=lv;   break;
    case kwCase:  lcs="KWCASE";   lvs=lv;   break;
    case kwEnd:   lcs="KWEND";    lvs=lv;   break;
    case kwFloat: lcs="KWFLOAT";  lvs=lv;   break;
    case kwGoto:  lcs="KWGOTO";   lvs=lv;   break;
    case kwInt:   lcs="KWINT";    lvs=lv;   break;
    case kwLoop:  lcs="KWLOOP";   lvs=lv;   break;
    case kwOr:    lcs="KWOR";     lvs=lv;   break;
    case kwRead:  lcs="KWREAD";   lvs=lv;   break;
    case kwSkip:  lcs="KWSKIP";   lvs=lv;   break;
    case kwSpace: lcs="KWSPACE";  lvs=lv;   break;
    case kwTab:   lcs="KWTAB";    lvs=lv;   break;
    case kwVar:   lcs="KWVAR";    lvs=lv;   break;
    case kwWrite: lcs="KWWRITE";  lvs=lv;   break;
    default:      lcs="nonprinted lex class"; lvs=lv;
  }
  fprintf(f, "[%d, %d] lc: %s\t\tlv: %s\n", line, column, lcs, lvs);  
}
