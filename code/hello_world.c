#include <stdio.h>
#include <string.h>
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>

#define OFFSET -32
#define PWM_PERIOD 16

alt_8 pwm = 0;
alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

float filter_FIR(alt_32 x_values[], int size){
    int res = 0;
    int coeff[49] = {4, 6, -4,	-8,	2,	0,	-10,	2,	4,	-14,	2,	10,	-18,	-2,	22,	-24,	-12,	38,	-28,	-34,	74,	-30,	-122,	286,	636,	286,	-122,	-30,	74,	-34,	-28,	38,	-12,	-24, 22, -2,	-18, 10, 2, -14, 4, 2, -10, 0, 2, -8, -4, 6, 4};

    for(int i = 0; i < size; i++)
    {
        res += x_values[i]*coeff[i];
    }
    return res/1000;
}

int main()
{
    const int N = 49;   // number of taps in FIR filter
    alt_32 x_values[N];
    float filtered;
    for(int i = 0; i < N; i++){     //initialise x_values with 0s
    	x_values[i] = 0;
    }

    alt_32 x_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL){      // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }

    timer_init(sys_timer_isr);

	printf("Running..\n");
	FILE* fp, data;
	char prompt = 0;

    data = fopen("data/data.txt", "w");
    if(f == NULL){
        printf("Error opening file\n");
        exit(1);
    }

	fp = fopen ("/dev/jtag_uart", "r+"); 	    // create file pointer to jtag_uart port
	if (fp){
		while (prompt != 'v'){      // here 'v' is used as the character to stop the program
			prompt = getc(fp);      // accept the character that has been sent down
			if (prompt != 'v') {
				alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);

                for(int i = 0; i < N; i++){
                x_values[i] = x_values[i+1];
                }
                x_values[N-1] = x_read;
                filtered = filter_FIR(x_values, N);

                convert_read(filtered, & level, & led);

                alt_fprintf(data, "raw data: %x\n", x_read);
                alt_printf("raw data: %x\n", x_read);
			}
			if (ferror(fp)) {
				clearerr(fp);
			}
		}
		fprintf(fp, "Closing the JTAG UART file handle.\n %c",0x4);
		fclose(fp);
        fclose(data);
	}
	printf("Complete\n");

	return 0;
}
