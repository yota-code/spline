#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>

#define pixel_addr(x, y) (self->data + ((x) + self->radius) + (((y) + self->radius) * self->length))

#define foreach_xy(code) {\
	for (int x= -1 * self->radius ; x <= self->radius ; x++) {\
		for (int y=  -1 * self->radius ; y <= self->radius ; y++) {\
			code \
		} \
	} \
}

typedef struct {
	/* patch is a pixel centric portion of the image */
	double * data;
	int radius;
	int length;
} patch_C;

int patch_debug(patch_C * self) {
	double z;
	for (unsigned int i=0 ; i<self->length ; i++) {
		for (unsigned int j=0; j<self->length ; j++) {
			z = *(self->data + i + (j * self->length));
			/*z = z * 16.0;
			z = z > 15.0 ? 15.0 : z;
			z = z < 0.0 ? 0.0 : z;
			printf("%2X", (unsigned int)(z) & 0xF);
			z = z > 1.0 ? 1.0 : z;
			z = z < 0.0 ? 0.0 : z;*/
			printf("%0.1f\t", z);
		}
		printf("\n");
	}
			
}

patch_C patch__new__(unsigned int radius) {
	patch_C m;
	
	m.radius = radius;
	m.length = (2 * m.radius + 1);
	m.data = calloc(sizeof(double), m.length);
	
	return m;
}

int patch__del__(patch_C * self) {
	free(self->data);
	free(self);
	return EXIT_SUCCESS;
}

double patch_set_pixel(patch_C * self, int x, int y, double z) {
	assert(! ((abs(x) > self->radius) || (abs(y) > self->radius)));
	//printf("set_pixel(@%08x + %08x, %f)\n", self->data, pixel_addr(x, y) - self->data, z);
	*(pixel_addr(x, y)) = z;
}

double patch_get_pixel(patch_C * self, int x, int y) {
	assert(! ((abs(x) > self->radius) || (abs(y) > self->radius)));
	//printf("set_pixel(@%08x + %08x)\n", self->data, pixel_addr(x, y) - self->data);
	return *(pixel_addr(x, y));
}

double dist(double x, double y, double norm) {
	return pow(pow(fabs(x), norm) + pow(fabs(y), norm), 1.0 / norm);
}

int patch_normalize(patch_C * self) {
	double x, y, z, n;
	n = patch_get_pixel(self, 0, 0);
	assert(n != 0.0);
	for (double i=0.0 ; i<self->length ; i+=1.0) {
		x = i - self->radius;
		for (double j=0.0; j<self->length ; j+=1.0) {
			y = j - self->radius;
			/* -------- */
			z = patch_get_pixel(self, x, y);
			patch_set_pixel(self, x, y, z / n);
			/* -------- */
		}
	}
}



int patch_mask(patch_C * self, double threshold) {
	double d;
	foreach_xy(
		z = patch_get_pixel(x, y);
		patch_set_pixel(self, x, y, (z <= threshold) ? 1.0 : 0.0);
	)
	return EXIT_SUCCESS;
}

int patch_distance(patch_C * self, double norm) {
	double d;
	foreach_xy(
		d = dist(x, y, norm);
		patch_set_pixel(self, x, y, d);
	)
	return EXIT_SUCCESS;
}
	
int main(int argc, char * argv[]) {
	
	patch_C m, n;
	m = patch__new__(5);
	//patch_set_pixel(&m, 0, 0, 0.7);
	//patch_draw_mask(&m, 5.1, 0.8);
	patch_draw_distance(&m, 0.8);
	printf("get_pixel() -> %f\n", patch_get_pixel(&m, 0, 0));
	patch_debug(&m);
	
}
