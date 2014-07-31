#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>


/**************************************************

 map a file to an executable memory page and call it.
 Useful for testing shellcode.

	gcc runasm.c -o runasm 
	nasm helloworld.s
	runasm helloworld

	if you want to debug the shellcode, prefix a \xcc and run under gdb

**************************************************/



int main(int argc, char *argv[]) {

	int fdin = 0;
	off_t size;
	void (*shellcode)() = NULL; // shellcode is a pointer to a function that has no arguments

	/* check usage */


	/* open the input file */
	fdin = open(argv[1], O_RDONLY);
	if (fdin < 0) {
		fprintf(stderr, "Error opening %s for reading\n", argv[1]);
		return 1;
	}	

	/* find size of input file */
	size = lseek(fdin, 0, SEEK_END);
	if (size <= 0) {
		fprintf(stderr, "File (fd == %x) size error: %x\n", fdin, (unsigned int)size);
		return 1;
	}
	lseek(fdin, 0, SEEK_SET);

	/* mmap the file to a new page and make it executable */
	shellcode = mmap(NULL, (int)size, PROT_EXEC | PROT_READ | PROT_WRITE, MAP_PRIVATE, fdin, 0);
	close(fdin);
	
	if (shellcode == MAP_FAILED) {
		fprintf(stderr, "Failed to mmap %x bytes at %p\n", (int)size, shellcode);
	}

	/* jmp to the shellcode */
	shellcode();
	return 0;

}

