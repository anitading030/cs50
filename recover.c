#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //correct length of input
    if (argc != 2)
    {
        return 1;
    }

    //open file
    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        return 2;
    }


    int sequence = 0;          //count image numbers
    unsigned char buffer[512];          //create buffer for every 512 bytes
    FILE *img;          //file I will write into
    char new_file[7];          //format of the fileneme for each image recovered, "###.jpg"


    //read every 512 bytes into a buffer until the end of memory
    while (fread(buffer, 512, 1, file))
    {
        //if first 4 bytes of a buffer meet conditions, then it is the start of a new jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if it is the first file, create 000.jpg
            if (sequence == 0)
            {
                sprintf(new_file, "%03i.jpg", sequence);
                img = fopen(new_file, "w");
                fwrite(buffer, 512, 1, img);
                sequence += 1;
            }

            //if there is already an old new file
            else
            {
                //close previous image
                fclose(img);

                //start writing to a new file
                sprintf(new_file, "%03i.jpg", sequence);
                img = fopen(new_file, "w");
                fwrite(buffer, 512, 1, img);
                sequence += 1;
            }
        }

        //if not the start of a new jpeg file, keep writing to the old one
        else
        {
            fwrite(buffer, 512, 1, img);
        }

    }
}
