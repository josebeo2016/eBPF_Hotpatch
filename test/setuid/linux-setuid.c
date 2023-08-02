/*
	Created @ 03.02.2014
	Copyright (C) 2014 Christian Mayer <http://fox21.at>
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
	
// Reference from: https://gist.github.com/mprota/1ffde8bf3e2247252bdac633ba2140b1

#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>

int main(){
	printf("start\n");
	
	printf("sleep\n"); 
    usleep(1000 * 1000);
	
    int retval;
	uid_t uid = 1000; // user
	//gid_t gid = 100;  // users

    printf("The uid that you enter is: %d\n", uid);
	
    retval = -EPERM;
    int result = setuid(uid);
    if (result < 0) {
		printf("exit with error %d\n", retval);
        return retval;
    }
	//printf("sleep\n"); usleep(10 * 1000 * 1000);
	
	//printf("setgid: %d\n", gid);
	//setgid(gid);
	
	printf("exit without error\n");
    return 0;
}