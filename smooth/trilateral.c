#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>

typedef int32_t fp_t; /* 12.20 */
typedef int64_t buff_t;

typedef struct {
	uint32_t w;
	uint32_t h;
	fp_t * a;
} img_t;

#define fp_set(a) (fp_t)((double)(a) * 0x00100000)
#define fp_get(a) ((double)(a) / 0x00100000)

#define fp_add(a, b) ((a) + (b))
#define fp_sub(a, b) ((a) - (b))

#define fp_opp(a) (- (a))
#define fp_inv(a) (fp_set(1.0 / fp_get(a)))

#define fp_dst(a, b) ((a) > (b) ? fp_sub(a, b) : fp_sub(b, a))

#define fp_mul(a, b) ((fp_t)((((buff_t)(a) * (buff_t)(b)) >> 20) & 0xFFFFFFFF))
#define fp_div(a, b) ((fp_t)(((((buff_t)(a) << 20) / (buff_t)(b))) & 0xFFFFFFFF))

img_t * img_new(size_t width, size_t height) {
	
	img_t * self;
	
	self = malloc(1 * sizeof(img_t));
	
	self->h = height;
	self->w = width;
	self->a = malloc(width * height * sizeof(fp_t));
	
	return self;
	
}

int img_del(img_t * self) {

	free(self->a);
	free(self);
	
}

img_t *  img_loadfile(char * path) {
	
	FILE * fid;
	int exit = EXIT_FAILURE;
	
	img_t * self = NULL;
	
	if (fid = fopen(path, "rb")) {
		if (
			(fread(&(self->w), sizeof(uint32_t), 1, fid) == sizeof(uint32_t)) &&
			(fread(&(self->h), sizeof(uint32_t), 1, fid) == sizeof(uint32_t))
		) {
			self = img_new(self->w, self->h);
			exit = fread(self->a, sizeof(fp_t), self->w * self->h, fid) == self->w * self->h * sizeof(fp_t);
		}
		fclose(fid);
	}
	
	if (exit != EXIT_SUCCESS) {
		img_del(self);
		return NULL;
	}
	
	return self;
	
}
	


int main(int argc, char * argv[]) {
	
	fp_t a = fp_set(2.0);
	fp_t b = fp_set(-3.0);
	
	fprintf(stdout, "a= %f\n", fp_get(a));
	fprintf(stdout, "b= %f\n", fp_get(b));
	fprintf(stdout, "add= %f\n", fp_get(fp_add(a, b)));
	fprintf(stdout, "sub= %f\n", fp_get(fp_sub(a, b)));
	fprintf(stdout, "opp= %f\n", fp_get(fp_opp(b)));
	fprintf(stdout, "inv= %f\n", fp_get(fp_inv(b)));
	fprintf(stdout, "mul= %f\n", fp_get(fp_mul(a, b)));
	fprintf(stdout, "div= %f\n", fp_get(fp_div(a, b)));
	fprintf(stdout, "dst= %f\n", fp_get(fp_dst(a, b)));
	
}
