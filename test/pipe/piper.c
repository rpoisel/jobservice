#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void Child_write  (pid_t Handle);
void Parent_write (pid_t Handle, char c);
void Child_read  (pid_t Handle);
void Parent_read (pid_t Handle);

void main()
{

    pid_t Pid;
    int   writepipe[2],readpipe [2];  

    pipe(readpipe);               /* Create two file descriptors  */
    pipe(writepipe);              /* Create two file descriptors  */

    Pid = fork();

    if (Pid == 0)         
    {
        close(writepipe[1]);               /* closing writepipe's write end */
        dup2(writepipe[0],0); close(writepipe[0]);     /* duplicating writepipe's read    end to stdin*/
        close(readpipe[0]);                /* closing readpipe's read end*/
        dup2(readpipe[1],1);  close(readpipe[1]);      /* duplicating readpipe's write end to stdout*/    
        Child_read(writepipe[0]);              /* reading data from write pipe read end and then duplicating*/

    }
    else                  
    {
        close(writepipe[0]);               /* closing writepipe's read end */
        Parent_write(writepipe[1],'1');            /* pupming data to the writepipe */
        close(readpipe[1]);                /* closing the readpipes write end */
        Parent_read(readpipe[0]);              /* reading the data which is pumped into readpipe */
        //Parent_write(writepipe[1],'2');          /* pupming data to the writepipe */
        //Parent_read(readpipe[0]);

        //Parent_write(writepipe[1],'3');
        //Parent_read(readpipe[0]);
        puts("***** End of parent process*****");
    }
}

void Child_read(pid_t handle)
{
    static char* command = "./external";
    execvp(command, NULL);
}

void Parent_write(pid_t handle, char c)
{
    char Buff[] = {'\n','\n'};
    Buff[0] = c;
    int n_written= write(handle, Buff, strlen(Buff)+1);

    printf("write function has written %d no of bytes and the data written is %s",n_written,Buff);

    //close(handle);
}

void Parent_read(pid_t handle)
{
    printf("PARENT PROCESS: In Parent_read function\n");
    int i=0;
    int bytes_read = 0;
    char buffer[1024]= {'\0'};
    while (read(handle, buffer, sizeof(buffer)) > 0)
    {
        printf("PARENT PROCESS:: In while loop\n");
        printf("The character/string read from readend of readpipe (stdout) is %s",buffer);
    }
    close(handle);
}
