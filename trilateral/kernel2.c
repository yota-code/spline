#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>

#define KERNEL_RADIUS 3
#define KERNEL_WIDTH ((KERNEL_RADIUS * 2) + 1)
#define KERNEL_LENGTH (KERNEL_WIDTH * KERNEL_WIDTH)

typedef struct {
	int x;
	int y;
} pos_T;

typedef double pix_T;

/*#define sn_get(i) int x = snake[i].x; int y = snake[i].y*/
#define sq_(x, y) square[x+KERNEL_RADIUS][y+KERNEL_RADIUS]
#define c_(a, x, y) a[(x+KERNEL_RADIUS) + ((y+KERNEL_RADIUS)*KERNEL_WIDTH)]

#define foreach(code) {\
	for (int i=0 ; i < KERNEL_LENGTH ; i++) { \
		int x = snake[i].x; int y = snake[i].y; \
		code \
	} \
}

pos_T * pointer_spiral(size_T radius) {
	int x=0, y=0;
	int dx=0, dy=-1, b=0;
	size_T width=(radius * 2) + 1;
	size_T length=width * width;
	pos_T * m;
	m = calloc(sizeof(pix_T), kernel_length);
	for (int i=0 ; i<kernel_length ; i++) {
		if ((x == y) || (x < 0 && x == -y) || (x > 0 && x == 1-y)) {
			b = dx; dx = -dy; dy = b;
		}
		x += dx;
		y += dy;
		//printf("%d %d %d\n", i, x, y);
		m[i].x = x;
		m[i].y = y;
	}
	return m;
}

pos_T * pointer_scanline(size_T kernel_length) {
	int x=0, y=0;
	int dx=0, dy=-1, b=0;
	pos_T * m;
	m = calloc(sizeof(pix_T), kernel_length);
	for (int i=0 ; i<kernel_length ; i++) {
		if ((x == y) || (x < 0 && x == -y) || (x > 0 && x == 1-y)) {
			b = dx; dx = -dy; dy = b;
		}
		x += dx;
		y += dy;
		//printf("%d %d %d\n", i, x, y);
		m[i].x = x;
		m[i].y = y;
	}
	return m;
}


double _distance(double x, double y, double norm) {
	return pow(pow(fabs(x), norm) + pow(fabs(y), norm), 1.0 / norm);
}

int square_distance(pix_T * m, double norm) {
	foreach(
		c_(m, x, y) = _distance(x, y, norm);
	);
	return EXIT_SUCCESS;
}

int square_normalize(pix_T square[KERNEL_WIDTH][KERNEL_WIDTH], pos_T snake[KERNEL_LENGTH]) {
	pix_T n = sq_(0, 0);
	assert(n != 0.0);
	foreach(
		sq_(x, y) = sq_(x, y) / n;
	);
}

/*int square_sum(pix_T * square[KERNEL_WIDTH][KERNEL_WIDTH], pos_T snake[KERNEL_LENGTH]) {
	pix_T z = 0.0;
	foreach(
		z += sq_(x, y);
	);
}*/

int square_threshold(pix_T square[KERNEL_WIDTH][KERNEL_WIDTH], pos_T snake[KERNEL_LENGTH], double value) {
	/* if pixel value is lower than threshold value, set 1.0, else set 0.0 */
	foreach(
		sq_(x, y) = sq_(x, y) <= value ? 1.0 : 0.0;
	);
	return EXIT_SUCCESS;
}

int main(int argc, char * argv[]) {
	pix_T a[KERNEL_WIDTH][KERNEL_WIDTH];
	pos_T b[KERNEL_LENGTH];
	
	printf("KERNEL_RADIUS %d\n", KERNEL_RADIUS);
	printf("KERNEL_WIDTH %d\n", KERNEL_WIDTH);
	printf("KERNEL_LENGTH %d\n", KERNEL_LENGTH);
	
	snake_spiral(b);
	square_distance(a, 1.2);
	
	return EXIT_SUCCESS;
}
