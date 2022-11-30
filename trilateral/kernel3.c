#define _GNU_SOURCE

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <string.h>

#define max(x, y) ((x) > (y) ? (x) : (y))

typedef double real_T;
typedef unsigned char bool_T;

typedef struct {
	int x;
	int y;
} pos_T;

typedef struct {
	/* ax + by + cz + d = 0, normal vector [a, b, c] */
	real_T a;
	real_T b;
	real_T c;
	real_T d;
} plane_T;

typedef struct {
	real_T x;
	real_T y;
	real_T z;
} vec3_T;

typedef struct {
	size_t radius;
	size_t width;
	size_t length;
	pos_T * pointer;
	real_T * value;
	real_T * mask;
} kernel_C;

pos_T * kernel_pointer = NULL;

#define get_(k, a, x, y) ((k)->a[(x + ((k)->radius)) + ((y + ((k)->radius)) * ((k)->width))])

#define v_(k, x, y) ((k)->value[(x + ((k)->radius)) + ((y + ((k)->radius)) * ((k)->width))])
#define m_(k, x, y) ((k)->mask[(x + ((k)->radius)) + ((y + ((k)->radius)) * ((k)->width))])

#define foreach(code) {\
	for (int _iter_=0 ; _iter_ < self->length ; _iter_++) { \
		int x = self->pointer[_iter_].x; int y = self->pointer[_iter_].y; \
		code \
	} \
}

kernel_C kernel__new__(size_t radius) {
	kernel_C new;
	new.radius = radius;
	new.width = (2*(new.radius)) + 1;
	new.length = new.width*new.width;
	new.pointer = calloc(sizeof (pos_T), new.length);
	new.kernel = calloc(sizeof (real_T), new.length);
	new.mask = calloc(sizeof (real_T), new.length);
	return new;
}

int kernel__del__(kernel_C * self) {
	free(self->kernel);
	free(self);
	return EXIT_SUCCESS;
}

int _compare(void const * a, void const * b) {
   real_T const * pa = a;
   real_T const * pb = b;
   return (* pa) - (* pb);
}

real_T quantile(real_T * array, size_t len, real_T q) {
	real_T a, b, i;
	real_T * buffer = malloc(sizeof (real_T) * len);
	memcpy(buffer, array, sizeof (real_T) * len);
	qsort(buffer, len, sizeof (real_T), _compare);
	i = q * (len - 1);
	a = floor(i);
	b = ceil(i);
	// printf("a:%f b:%f i:%f\n", a, b, i);
	if (a == b) {
		return buffer[(int) i];
	} else {
		return (buffer[(int) a] * (b - i)) + (buffer[(int) b] * (i - a));
	}
}

real_T kernel_quantile(kernel_C * self, real_T q) {
	return quantile(self->kernel, self->length, q);
}

int kernel_square_sort(kernel_C * self) {
	qsort(self->kernel, self->length, sizeof (real_T), _compare);
	return EXIT_SUCCESS;
}


int image__load__(kernel_C * self, char * filename) {
	FILE * fid;
	size_t len;
	char * buffer, * cell;
	int x = - self-> radius, y = self-> radius;
	real_T value;
	
	fid = fopen(filename, "rt");
	if (fid == NULL) { return EXIT_FAILURE; }
	
	fseek(fid , 0 , SEEK_END);
	len = ftell(fid);
	rewind(fid);
	
	buffer = malloc(sizeof (char) * len);
	fread(buffer, 1, len, fid);
	
	cell = &(buffer[0]);
	for (size_t i=0 ; i<len ; i++) {
		if (buffer[i] == '\t' || buffer[i] == '\n') {
			sscanf(cell, "%lf", &value);
			//printf("%d %d -> %f\n", x, y, value);
			k_(self, x, y) = value;
			if (buffer[i] == '\t') {
				x += 1;
			}
			if (buffer[i] == '\n') {
				y -= 1;
				x = - self->radius;
			}
			cell = &(buffer[i+1]);
		}
	}
	
	fclose(fid);
	free(buffer);
}

int kernel_square__dump__(kernel_C * self, char * filename) {
	/* open filename, dump the values of the kernel */
	FILE * fid;
	size_t len;
	
	fid = fopen(filename, "wt");
	if (fid == NULL) {
		return EXIT_FAILURE;
	}
	for (size_t i=0 ; i<self->width ; i++) {
		for (size_t j=0; j<self->width ; j++) {
			fprintf(fid, "%0.1f", self->kernel[j + ((self->width - i - 1) * self->width)]);
			if (j < self->width - 1) {
				fprintf(fid, "\t");
			}
		}
		fprintf(fid, "\n");
	}
	fclose(fid);
	return EXIT_SUCCESS;
}


kernel_C  kernel__copy__(kernel_C * self) {
	kernel_C copy = * self;
	
	copy.kernel = calloc(sizeof(real_T), copy.length);
	memcpy(copy.kernel, self->kernel, sizeof(real_T) * copy.length);
	
	return copy;
}

int kernel_pointer__display__(kernel_C * self) {
	for (int i=0 ; i<self->length ; i++) {
		printf("%3d %3d\n", self->pointer[i].x, self->pointer[i].y);
	}
	return EXIT_SUCCESS;
}

int kernel_square__display__(kernel_C * self) {
	for (size_t i=0 ; i<self->width ; i++) {
		for (size_t j=0; j<self->width ; j++) {
			fprintf(stdout, "%0.1f", self->kernel[j + ((self->width - i - 1) * self->width)]);
			if (j < self->width - 1) {
				fprintf(stdout, "\t");
			}
		}
		fprintf(stdout, "\n");
	}
	fprintf(stdout, "------\n");
	for (size_t i=0 ; i<self->width ; i++) {
		for (size_t j=0; j<self->width ; j++) {
			fprintf(stdout, "%0.1f", self->mask[j + ((self->width - i - 1) * self->width)]);
			if (j < self->width - 1) {
				fprintf(stdout, "\t");
			}
		}
		fprintf(stdout, "\n");
	}
	return EXIT_SUCCESS;
}


int kernel_pointer_scanline(kernel_C * self) {
	for (int i=0 ; i<self->length ; i++) {
		self->pointer[i].x = i % self->width;
		self->pointer[i].y = i / self->width;
	}
	return EXIT_SUCCESS;
}

int pointer_set_spiral(kernel_C * self) {
	int x = 0, y = 0;
	int dx = 0, dy = -1, b = 0;
	for (int i=0 ; i<self->length ; i++) {
		if ((x == y) || (x < 0 && x == -y) || (x > 0 && x == 1-y)) {
			b = dx; dx = -dy; dy = b;
		}
		self->pointer[i].x = x;
		self->pointer[i].y = y;
		x += dx; y += dy;
	}
	return EXIT_SUCCESS;
}

double _distance2(double x, double y, double norm) {
	return pow(pow(fabs(x), norm) + pow(fabs(y), norm), 1.0 / norm);
}

double _distance3(double x, double y, double z, double norm) {
	return pow(pow(fabs(x), norm) + pow(fabs(y), norm) + pow(fabs(z), norm), 1.0 / norm);
}

int kernel_square_distance(kernel_C * self, double norm) {
	foreach(
		k_(self, x, y) = _distance2(x, y, norm);
	);
	return EXIT_SUCCESS;
}

//int kernel_square_halo(kernel_C * self, double norm, ) {
//	foreach(
//		/* to be implemented as x^2 * exp(-(x^2)) */
//	);
//	return EXIT_SUCCESS;
//}

int mask_set_circle(kernel_C * self, double radius, double norm) {
	real_T d;
	foreach(
		d = _distance2(x, y, norm);
		m_(self, x, y) = (d <= radius) ? 1.0 : 0.0;
	)
}


int kernel_square_normalize_center(kernel_C * self) {
	real_T n = k_(self, 0, 0);
	assert(n != 0.0);
	foreach(
		k_(self, x, y) = k_(self, x, y) / n;
	);
}

int kernel_square_normalize(kernel_C * self, double n) {
	assert(n != 0.0);
	foreach(
		k_(self, x, y) = k_(self, x, y) / n;
	);
}

double kernel_square_max(kernel_C * self) {
	/* return the highest pixel value */
	real_T z;
	foreach(
		z = max(z, k_(self, x, y));
	);
}

double kernel_square_sum(kernel_C * self) {
	/* return the sum of all pixel values */
	real_T z;
	foreach(
		z += k_(self, x, y);
	);
}

int kernel_square_normalize_max(kernel_C * self) {
	real_T n = kernel_square_max(self);
	assert(n != 0.0);
	foreach(
		k_(self, x, y) = k_(self, x, y) / n;
	);
}

int kernel_square_where_lower_equal(kernel_C * self, double value) {
	/* if pixel value is lower than threshold value, set 1.0, else set 0.0 */
	foreach(
		k_(self, x, y) = k_(self, x, y) <= value ? 1.0 : 0.0;
	);
	return EXIT_SUCCESS;
}

plane_T kernel_square_average_gradient(kernel_C * self) {
	/* retourne les coordonnées du plan moyen */
	real_T a = 0.0, b = 0.0, c = 0.0, g;
	real_T d = k_(self, 0, 0);
	foreach(
		g = k_(self, x, y) - d;
		a += -1.0 * g * x;
		b += -1.0 * g * y;
		c += _distance2(x, y, 2.0);
	);
	g = _distance3(a, b, c, 2.0);
	a /= g;
	b /= g;
	c /= g;
	printf("gradient() = %f %f %f (%f)\n", a, b, c, g);
	return (plane_T) {a, b, c, d};
}

plane_T patch_biased_gradient(kernel_C * self, plane_T p) {
	/* retourne les coordonnées du plan moyen, pondérée par la distance au plan proposé */
	real_T e = _distance3(p.a, p.b, p.c, 2.0);
	vec3_T g = {0.0, 0.0, 0.0};
	plane_T q = {0.0, 0.0, 0.0, 0.0};
	real_T d, m, n;
	
	q.d = k_(self, 0, 0);
	foreach(
		/* distance of a point to a plane */
		d = ((p.a*x) + (p.b*y) + (p.c*k_(self, x, y)) + p.d) / e;
		/* mask and distance bias */
		m = m_(self, x, y) * (1.0/(1.0 + pow(d, 2.0)));
		/* relative value */
		n = k_(self, x, y) - q.d;
		
		q.a += -1.0 * n * x * m;
		q.b += -1.0 * n * y * m;
		q.c += _distance2(x, y, 2.0) * m;
	)
	
	/* normalization */
	d = _distance3(q.a, q.b, q.c, 2.0);
	q.a /= d;
	q.b /= d;
	q.c /= d;
	
	printf("patch_biased_gradient() => %f %f %f %f\n", q.a, q.b, q.c, q.d);
	return q;
}

plane_T patch_iterative_gradient(kernel_C * self, int c) {
	plane_T p = {0.0, 0.0, 1.0, k_(self, 0, 0)};
	
	for(int i=0 ; i < c ; i++ ) {
		p = patch_biased_gradient(self, p);
	}
}
	

real_T g3_distance_to_plane(plane_T p, vec3_T m) {
	/* calcule la distance d'un point à un plan */
	return (p.a * m.x) + (p.b * m.y) + (p.c * m.z) + p.d;
}

real_T kernel_square_trilateral(kernel_C * self) {
	
	
}

int main(int argc, char * argv[]) {
	kernel_C u, v;
	
	u = kernel__new__(3);
	pointer_set_spiral(&u);
	mask_set_circle(&u, 3.0, 2.0);
	image__load__(&u, "corner_wall.dat");
	
	kernel_square__display__(&u);

	patch_iterative_gradient(&u, 50);
	
	//kernel_pointer__display__(&u);
	
	//for (int i=0 ; i< 100000 ; i++) {
	//kernel_square_distance(&u, 3.0);
	//}
	
	//real_T a[] = {0.0, 0.0, 1.0, 2.0, 2.0, 3.0, 4.0, 6.0, 9.0, 10.0, 11.0};
	//printf("quantile: %f\n", quantile(a, 11, 0.5));
	
	//k_(&u, 0, 0) = 2.0;
	//kernel_square_normalize_max(&u);
	//v = kernel__copy__(&u);
	//kernel_square_sum(&u);
	
	/*kernel_square__display__(&u);
	image__load__(&u, "src.dat");
	kernel_square__display__(&u);
	kernel_square__dump__(&u, "dst.dat");*/
	
	//image__load__(&u, "top_left_hill.dat");
	//kernel_square_gradient(&u);
	
	//kernel_set_radius(3);
	//pointer_scanline();
	//
	//printf("kernel_radius %d\n", kernel_radius);
	//printf("kernel_width %d\n", kernel_width);
	//printf("kernel_length %d\n", kernel_length);
	//
	//pointer__display__();
	
	return EXIT_SUCCESS;
}
