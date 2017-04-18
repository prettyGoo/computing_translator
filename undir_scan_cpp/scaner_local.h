//------------------------------------------------------------------------------
// scaner_local.h - описание типов данных, используемых только сканером
//------------------------------------------------------------------------------

struct find_string {
    char* wrd;   
    lc_type lc;
};


struct find_string rwtab[] = {
    {"abort", kwAbort},
    {"begin", kwBegin},
    {"case",  kwCase},
    {"end",   kwEnd},
    {"float", kwFloat},
    {"goto",  kwGoto},
    {"int",   kwInt},
    {"loop",  kwLoop},
    {"read",  kwRead},
    {"skip",  kwSkip},
    {"space", kwSpace},
    {"tab",   kwTab},
    {"var",   kwVar},
    {"write", kwWrite}
};

int rw_size = sizeof(rwtab) / sizeof(find_string);

long int poz=0, oldpoz;
int oldline, oldcolumn;
