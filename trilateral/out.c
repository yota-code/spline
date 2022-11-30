



























extern unsigned char __ctype[];

typedef struct {
 int quot;
 int rem;
} div_t;

typedef struct {
 long quot;
 long rem;
} ldiv_t;






typedef unsigned int size_t;

typedef long wchar_t;





extern void abort(void);
extern int abs(int);
extern int atexit(void (*)(void));
extern double atof(const char *);
extern int atoi(const char *);
extern long int atol(const char *);
extern void *bsearch(const void *, const void *, size_t, size_t,
 int (*)(const void *, const void *));
extern void *calloc(size_t, size_t);
extern div_t div(int, int);
extern void exit(int);
extern void free(void *);
extern char *getenv(const char *);
extern long int labs(long);
extern ldiv_t ldiv(long, long);
extern void *malloc(size_t);
extern int mblen(const char *, size_t);
extern size_t mbstowcs(wchar_t *, const char *, size_t);
extern int mbtowc(wchar_t *, const char *, size_t);
extern void qsort(void *, size_t, size_t,
 int (*)(const void *, const void *));
extern int rand(void);
extern void *realloc(void *, size_t);
extern void srand(unsigned int);
extern double strtod(const char *, char **);
extern long int strtol(const char *, char **, int);
extern unsigned long int strtoul(const char *, char **, int);
extern int system(const char *);
extern int wctomb(char *, wchar_t);
extern size_t wcstombs(char *, const wchar_t *, size_t);


typedef struct {
 long long quot;
 long long rem;
} lldiv_t;







typedef long uid_t;

extern void _exithandle(void);




extern double drand48(void);
extern double erand48(unsigned short *);
extern long jrand48(unsigned short *);
extern void lcong48(unsigned short *);
extern long lrand48(void);
extern long mrand48(void);
extern long nrand48(unsigned short *);
extern unsigned short *seed48(unsigned short *);
extern void srand48(long);
extern int putenv(char *);
extern void setkey(const char *);

typedef int ssize_t;



extern void swab(const char *, char *, ssize_t);





extern int mkstemp(char *);




extern int mkstemp64(char *);





extern long a64l(const char *);
extern char *ecvt(double, int, int *, int *);
extern char *fcvt(double, int, int *, int *);
extern char *gcvt(double, int, char *);
extern int getsubopt(char **, char *const *, char **);
extern int grantpt(int);
extern char *initstate(unsigned, char *, size_t);
extern char *l64a(long);
extern char *mktemp(char *);
extern char *ptsname(int);
extern long random(void);
extern char *realpath(const char *, char *);
extern char *setstate(const char *);
extern void srandom(unsigned);
extern int ttyslot(void);
extern int unlockpt(int);
extern void *valloc(size_t);




extern int dup2(int, int);
extern char *qecvt(long double, int, int *, int *);
extern char *qfcvt(long double, int, int *, int *);
extern char *qgcvt(long double, int, char *);
extern char *getcwd(char *, size_t);
extern const char *getexecname(void);
extern char *getlogin(void);
extern int getopt(int, char *const *, const char *);
extern char *optarg;
extern int optind, opterr, optopt;
extern char *getpass(const char *);
extern char *getpassphrase(const char *);
extern int getpw(uid_t, char *);
extern int isatty(int);
extern void *memalign(size_t, size_t);
extern char *ttyname(int);


extern long long atoll(const char *);
extern long long llabs(long long);
extern lldiv_t lldiv(long long, long long);
extern char *lltostr(long long, char *);
extern long long strtoll(const char *, char **, int);
extern unsigned long long strtoull(const char *, char **, int);
extern char *ulltostr(unsigned long long, char *);





typedef __builtin_va_list __gnuc_va_list;














typedef void *__va_list;





typedef struct __FILE __FILE;





struct __FILE
{




 ssize_t _cnt;
 unsigned char *_ptr;

 unsigned char *_base;
 unsigned char _flag;
 unsigned char _file;
 unsigned __orientation:2;
 unsigned __ionolock:1;
 unsigned __filler:5;
};


typedef long long __longlong_t;

typedef __FILE FILE;

typedef long fpos_t;

extern __FILE __iob[20];

extern int remove(const char *);
extern int rename(const char *, const char *);
extern FILE *tmpfile(void);
extern char *tmpnam(char *);
extern int fclose(FILE *);
extern int fflush(FILE *);
extern FILE *fopen(const char *, const char *);
extern FILE *freopen(const char *, const char *, FILE *);
extern void setbuf(FILE *, char *);
extern int setvbuf(FILE *, char *, int, size_t);

extern int fprintf(FILE *, const char *, ...);

extern int fscanf(FILE *, const char *, ...);

extern int printf(const char *, ...);

extern int scanf(const char *, ...);

extern int sprintf(char *, const char *, ...);

extern int sscanf(const char *, const char *, ...);
extern int vfprintf(FILE *, const char *, __va_list);
extern int vprintf(const char *, __va_list);
extern int vsprintf(char *, const char *, __va_list);
extern int fgetc(FILE *);
extern char *fgets(char *, int, FILE *);
extern int fputc(int, FILE *);
extern int fputs(const char *, FILE *);


extern int getc(FILE *);
extern int putc(int, FILE *);



extern int getchar(void);
extern int putchar(int);

extern char *gets(char *);
extern int puts(const char *);
extern int ungetc(int, FILE *);
extern size_t fread(void *, size_t, size_t, FILE *);
extern size_t fwrite(const void *, size_t, size_t, FILE *);
extern int fgetpos(FILE *, fpos_t *);
extern int fseek(FILE *, long, int);
extern int fsetpos(FILE *, const fpos_t *);
extern long ftell(FILE *);
extern void rewind(FILE *);


extern void clearerr(FILE *);
extern int feof(FILE *);
extern int ferror(FILE *);

extern void perror(const char *);


extern int __filbuf(FILE *);
extern int __flsbuf(int, FILE *);


typedef long off_t;







typedef __longlong_t off64_t;

typedef __longlong_t fpos64_t;

extern unsigned char _sibuf[], _sobuf[];

extern unsigned char *_bufendtab[];
extern FILE *_lastbuf;

extern void setbuffer(FILE *, char *, size_t);
extern int setlinebuf(FILE *);





extern int snprintf(char *, size_t, const char *, ...);




extern int vsnprintf(char *, size_t, const char *, __gnuc_va_list);

extern FILE *fdopen(int, const char *);
extern char *ctermid(char *);
extern int fileno(FILE *);

extern FILE *popen(const char *, const char *);
extern char *cuserid(char *);
extern char *tempnam(const char *, const char *);
extern int getopt(int, char *const *, const char *);

extern int getsubopt(char **, char *const *, char **);

extern char *optarg;
extern int optind, opterr, optopt;
extern int getw(FILE *);
extern int putw(int, FILE *);
extern int pclose(FILE *);







extern int fseeko(FILE *, off_t, int);
extern off_t ftello(FILE *);

extern FILE *fopen64(const char *, const char *);
extern FILE *freopen64(const char *, const char *, FILE *);
extern FILE *tmpfile64(void);
extern int fgetpos64(FILE *, fpos64_t *);
extern int fsetpos64(FILE *, const fpos64_t *);
extern int fseeko64(FILE *, off64_t, int);
extern off64_t ftello64(FILE *);















typedef union _h_val {
 unsigned long _i[sizeof(double) / sizeof(unsigned long)];
 double _d;
} _h_val;


extern const _h_val __huge_val;

extern double acos (double);
extern double asin (double);
extern double atan (double);
extern double atan2 (double, double);
extern double cos (double);
extern double sin (double);
extern double tan (double);

extern double cosh (double);
extern double sinh (double);
extern double tanh (double);

extern double exp (double);
extern double frexp (double, int *);
extern double ldexp (double, int);
extern double log (double);
extern double log10 (double);
extern double modf (double, double *);

extern double pow (double, double);
extern double sqrt (double);

extern double ceil (double);
extern double fabs (double);
extern double floor (double);
extern double fmod (double, double);


extern int signgam;







enum version {libm_ieee = -1, c_issue_4, ansi_1, strict_ansi};


extern const enum version _lib_version;




struct exception {
 int type;
 char *name;
 double arg1;
 double arg2;
 double retval;
};

extern double erf (double);
extern double erfc (double);
extern double gamma (double);
extern double hypot (double, double);
extern int isnan (double);
extern double j0 (double);
extern double j1 (double);
extern double jn (int, double);
extern double lgamma (double);
extern double y0 (double);
extern double y1 (double);
extern double yn (int, double);

extern double acosh (double);
extern double asinh (double);
extern double atanh (double);
extern double cbrt (double);
extern double logb (double);
extern double nextafter (double, double);
extern double remainder (double, double);
extern double scalb (double, double);

extern double expm1 (double);
extern int ilogb (double);
extern double log1p (double);
extern double rint (double);

extern int matherr (struct exception *);




extern double significand (double);




extern double copysign (double, double);
extern double scalbn (double, int);

extern float modff (float, float *);






















enum fp_direction_type {
 fp_nearest = 0,
 fp_tozero = 1,
 fp_positive = 2,
 fp_negative = 3
};

enum fp_precision_type {
 fp_extended = 0,
 fp_single = 1,
 fp_double = 2,
 fp_precision_3 = 3
};

enum fp_exception_type {
 fp_inexact = 0,
 fp_division = 1,
 fp_underflow = 2,
 fp_overflow = 3,
 fp_invalid = 4
};

enum fp_trap_enable_type {
 fp_trap_inexact = 0,
 fp_trap_division = 1,
 fp_trap_underflow = 2,
 fp_trap_overflow = 3,
 fp_trap_invalid = 4
};

enum fp_class_type {
 fp_zero = 0,
 fp_subnormal = 1,
 fp_normal = 2,
 fp_infinity = 3,
 fp_quiet = 4,
 fp_signaling = 5
};


typedef int sigfpe_code_type;

typedef void (*sigfpe_handler_type)();





extern sigfpe_handler_type sigfpe (sigfpe_code_type, sigfpe_handler_type);




typedef float single;                                                                                                     



typedef unsigned extended[3];


typedef long double quadruple;

typedef unsigned fp_exception_field_type;

typedef char decimal_string[512];


typedef struct {
 enum fp_class_type fpclass;
 int sign;
 int exponent;
 decimal_string ds;


 int more;


 int ndigits;


} decimal_record;

enum decimal_form {
 fixed_form,


 floating_form

};

typedef struct {
 enum fp_direction_type rd;

 enum decimal_form df;

 int ndigits;
} decimal_mode;

enum decimal_string_form {
 invalid_form,
 whitespace_form,
 fixed_int_form,
 fixed_intdot_form,
 fixed_dotfrac_form,
 fixed_intdotfrac_form,
 floating_int_form,
 floating_intdot_form,
 floating_dotfrac_form,
 floating_intdotfrac_form,
 inf_form,
 infinity_form,
 nan_form,
 nanstring_form
};

extern void single_to_decimal (single *, decimal_mode *, decimal_record *, fp_exception_field_type *);

extern void double_to_decimal (double *, decimal_mode *, decimal_record *, fp_exception_field_type *);

extern void extended_to_decimal (extended *, decimal_mode *, decimal_record *, fp_exception_field_type *);

extern void quadruple_to_decimal (quadruple *, decimal_mode *, decimal_record *, fp_exception_field_type *);


extern void decimal_to_single (single *, decimal_mode *, decimal_record *, fp_exception_field_type *);

extern void decimal_to_double (double *, decimal_mode *, decimal_record *, fp_exception_field_type *);

extern void decimal_to_extended (extended *, decimal_mode *, decimal_record *, fp_exception_field_type *);

extern void decimal_to_quadruple (quadruple *, decimal_mode *, decimal_record *, fp_exception_field_type *);


extern void string_to_decimal (char **, int, int, decimal_record *, enum decimal_string_form *, char **);

extern void func_to_decimal (char **, int, int, decimal_record *, enum decimal_string_form *, char **, int (*)(void), int *, int (*)(int));


extern void file_to_decimal (char **, int, int, decimal_record *, enum decimal_string_form *, char **, FILE *, int *);



extern char *seconvert (single *, int, int *, int *, char *);
extern char *sfconvert (single *, int, int *, int *, char *);
extern char *sgconvert (single *, int, int, char *);
extern char *econvert (double, int, int *, int *, char *);
extern char *fconvert (double, int, int *, int *, char *);
extern char *gconvert (double, int, int, char *);
extern char *qeconvert (quadruple *, int, int *, int *, char *);
extern char *qfconvert (quadruple *, int, int *, int *, char *);
extern char *qgconvert (quadruple *, int, int, char *);

extern char *ecvt (double, int, int *, int *);
extern char *fcvt (double, int, int *, int *);
extern char *gcvt (double, int, char *);





extern double atof (const char *);
extern double strtod (const char *, char **);











extern void __assert(const char *, const char *, int);






typedef struct {
 int x;
 int y;
} pos_T;

typedef double pix_T;

int snake_spiral(pos_T snake[(((3 * 2) + 1) * ((3 * 2) + 1))]) {
 int x=0, y=0;
 int dx=0, dy=-1, b;
 for (int i=0 ; i < (((3 * 2) + 1) * ((3 * 2) + 1)) ; i++) {
  if ((x == y) || (x < 0 && x == -y) || (x > 0 && x == 1-y)) {
   b = dx; dx = -dy; dy = b;
  }
  x += dx; y += dy;

  snake[i].x = x; snake[i].y = y;
 }
}

double _distance(double x, double y, double norm) {
 return pow(pow(fabs(x), norm) + pow(fabs(y), norm), 1.0 / norm);
}

int square_distance(pix_T square[((3 * 2) + 1)][((3 * 2) + 1)], pos_T snake[(((3 * 2) + 1) * ((3 * 2) + 1))], double norm) {
 { double z; for (int i=0 ; i < (((3 * 2) + 1) * ((3 * 2) + 1)) ; i++) { int x = snake[i].x; int y = snake[i].y; z = _distance(x, y, norm); square[x+3][y+3] = z; } } }



 return 0;
}


int main(int argc, char * argv[]) {
 pix_T a[((3 * 2) + 1)][((3 * 2) + 1)];
 pos_T b[(((3 * 2) + 1) * ((3 * 2) + 1))];

 printf("KERNEL_RADIUS %d\n", 3);
 printf("KERNEL_WIDTH %d\n", ((3 * 2) + 1));
 printf("KERNEL_LENGTH %d\n", (((3 * 2) + 1) * ((3 * 2) + 1)));

 snake_spiral(b);
 square_distance(a, b, 1.2);

 return 0;
}
