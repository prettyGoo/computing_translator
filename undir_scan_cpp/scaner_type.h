#ifndef __types__
#define __types__

//------------------------------------------------------------------------------
// main_t.h - содержит общие для всех типы данных
//------------------------------------------------------------------------------

typedef enum {
    tltLetter, tltDigit, tltSkip
} sic_type;

typedef enum {
  lexArrow,
  lexAssign,
  lexColon,
  lexComma,
  lexComment,
  lexEQ,  
  lexEof, 
  lexError, 
  lexFloat, 
  lexGE,  
  lexGT,  
  lexId,  
  lexIgnore,
  lexLE,
  lexLftRndBr,
  lexLftSqBr,
  lexLT,
  lexMinus,
  lexNE,
  lexPercent,
  lexPlus,
  lexSemicolon,
  lexSkip,
  lexSlash, 
  lexStar,
  lexString,
  lexRghRndBr,
  lexRghSqBr,
  lexInt,

  kwAbort,  
  kwBegin,  
  kwCase, 
  kwEnd,    
  kwFloat,  
  kwGoto,  
  kwInt,  
  kwLoop,
  kwOr,     
  kwRead,
  kwSkip, 
  kwSpace,  
  kwTab,    
  kwVar,  
  kwWrite
} lc_type;


#endif