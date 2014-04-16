#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h> 
#include <time.h>
#include <pthread.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#define SUCCESS 0
#define ERROR   1

#define SERVER_PORT 50007
#define MAX_MSG 256

/* auxillary functions to read newline-terminated strings from a file/socket */
int readnf (int, char *);
int readline(int, char *, int);

int server;         /* listening socket descriptor */


/**
 * cleanup() is called to kill the thread upon SIGINT. 
**/
void cleanup()
{
    close(server);
    pthread_exit(NULL);
    return;
} /* cleanup() */


/**
 * Thread handler for incoming connections...
**/
void handler(void * paramsd) {
    struct sockaddr_in cliAddr;
    char line[MAX_MSG];
    char reply[MAX_MSG];
    int i;
    int client_local;   /* keep a local copy of the client's socket descriptor */
    int addr_len;       /* used to store length (size) of sockaddr_in */
    time_t currtime;        
    char time_msg1[6] = {'/', 'T', 'I', 'M', 'E', '\n'};
    char time_msg2[6] = {'/', 'T', 'I', 'M', 'E', 13};
    char quit_msg1[6] = {'/', 'Q', 'U', 'I', 'T', '\n'};
    char quit_msg2[6] = {'/', 'Q', 'U', 'I', 'T', 13};
    char cmd[6];
     
    client_local = *((int *)paramsd); /* store client socket descriptor */
    addr_len = sizeof(cliAddr); /* store value of size of sockaddr_in */
    
    /* get clients name and store in cliAddr */
    getpeername(client_local, (struct sockaddr*)&cliAddr, &addr_len);	
    /* reset line */
    memset(line, 0, MAX_MSG);
    
    /* now read lines from the client socket */
    while(readnf(client_local, line)!=ERROR)  /* loop - read from socket */
    {
        if (!strcmp(line,""))   /* string must not be null string */
            break;
        
        for (i = 0; i<6; i++)   /* get first 6 chars of string, capitalize */
            cmd[i] = toupper(line[i]);
        /* Did client ask for time? */
        if (strncmp(cmd, time_msg1, 6) == 0 || strncmp(cmd, time_msg2, 6) == 0) {
            printf("socket status; %d\n",socket);
            printf("Received /TIME from %s:%d\n", inet_ntoa(cliAddr.sin_addr), ntohs(cliAddr.sin_port));
            time(&currtime);                  /* get current time */
            strcpy(reply, ctime(&currtime));  /* copy into string */
            send(client_local, reply, strlen(reply), 0); /* return current time to client */
        }
        /* Does client want to quit? */
        else if (strncmp(cmd, quit_msg1, 6) == 0 || strncmp(cmd, quit_msg2, 6) == 0)
        {
            printf("Received /QUIT from %s:%d\n", inet_ntoa(cliAddr.sin_addr), ntohs(cliAddr.sin_port));
            break;
        }
        else if (strlen(line) > 2)
        {
            strcpy(reply, "You:");
            strcat(reply, line);
            send(client_local, reply,strlen(reply),0);             
        }        
        /* reset line */
        memset(line,0,MAX_MSG);
    } /* while(readnf) */
    
    close(client_local);        
    return;
} /* handler() */

/* main function */
int main (int argc, char *argv[]) 
{
    int client;         /* client socket descriptor */
    int addr_len;       /* used to store length (size) of sockaddr_in */
    pthread_t thread;   /* thread variable */
    
    struct sockaddr_in cliAddr;   /* socket address for client */
    struct sockaddr_in servAddr;  /* socket address for server */

    signal(SIGINT, cleanup);      /* now handle SIGTERM and SIGINT */    
    signal(SIGTERM, cleanup);
  
    /* now create the server socket 
       make it an IPV4 socket (PF_INET) and stream socket (TCP)
       and 0 to select default protocol type */          
    server = socket(PF_INET, SOCK_STREAM, 0);
    if (server < 0) {
        perror("cannot open socket ");
        return ERROR;
    }
  
    /* now fill in values of the server sockaddr_in struct 
       s_addr and sin_port are in Network Byte Order (Big Endian)
       Since Intel CPUs use Host Byte Order (Little Endian), conversion 
       is necessary (e.g. htons(), and htonl() */    
    servAddr.sin_family = AF_INET;  /* again ipv4 */  
    servAddr.sin_addr.s_addr = htonl(INADDR_ANY); /* local address */
    servAddr.sin_port = htons(SERVER_PORT); 
    memset(servAddr.sin_zero, 0, 8);
        
    /* now bind server port 
       associate socket (server) with IP address:port (servAddr) */ 
    if (bind(server, (struct sockaddr *) &servAddr, sizeof(struct sockaddr)) < 0) {
        perror("cannot bind port ");
        return ERROR;
    }

    /* wait for connection from client with a pending queue of size 5 */
    listen(server, 5);
      
    while(1) /* infinite loop */
    {
        printf("%s: waiting for data on port TCP %u\n", argv[0], SERVER_PORT);
        addr_len = sizeof(cliAddr);
        
        /* new socket for client connection 
           accept() will block until a connection is present 
           accept will return a NEW socket for the incoming connection    
           server socket will continue listening 
           store client address in cliAddr */
        client = accept(server, (struct sockaddr *) &cliAddr, &addr_len);
        if (client < 0) {
            perror("cannot accept connection ");
            break;
        }
        pthread_create(&thread, 0, (void*)&handler, (void*) &client);
    } /* while (1) */

    close(server);
    exit(0);
} /* main() */


/** 
 * readnf() - reading from a file descriptor but a bit smarter 
**/
int readnf (int fd, char *line)
{
    if (readline(fd, line, MAX_MSG) < 0)
        return ERROR; 
    return SUCCESS;
}
  
/**
 * readline() - read an entire line from a file descriptor until a newline.
 * functions returns the number of characters read but not including the
 * null character.
**/
int readline(int fd, char *str, int maxlen) 
{
  int n;           /* no. of chars */  
  int readcount;   /* no. characters read */
  char c;

  for (n = 1; n < maxlen; n++) {
    /* read 1 character at a time */
    readcount = read(fd, &c, 1); /* store result in readcount */
    if (readcount == 1) /* 1 char read? */
    {
      *str = c;      /* copy character to buffer */
      str++;         /* increment buffer index */         
      if (c == '\n') /* is it a newline character? */
         break;      /* then exit for loop */
    } 
    else if (readcount == 0) /* no character read? */
    {
      if (n == 1)   /* no character read? */
        return (0); /* then return 0 */
      else
        break;      /* else simply exit loop */
    } 
    else 
      return (-1); /* error in read() */
  }
  *str=0;       /* null-terminate the buffer */
  return (n);   /* return number of characters read */
} /* readline() */
