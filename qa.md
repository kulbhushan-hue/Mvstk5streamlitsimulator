# MVS / TK5 Questions and Answers

### 1. What does `D A,L` show?
Active jobs and started tasks with job IDs and status.

### 2. What does `D ASM` show?
Auxiliary Storage Manager information such as paging and slot usage.

### 3. What does `D M=DEV` show?
Device status and descriptions.

### 4. What does `D VOLID` show?
Volume serial numbers, online status, device numbers, and device types.

### 5. What does `S` do?
Starts a procedure or started task.

### 6. What does `P` do?
Stops a procedure or started task.

### 7. What does `C job` do?
Cancels a job or started task.

### 8. What does `F job,parameter` do?
Sends a MODIFY command to an active job or started task.

### 9. What does `$DJ` show?
JES2 job status.

### 10. What does `$DI` show?
JES2 initiator status.

### 11. What does `$S INIT` do?
Starts a JES2 initiator.

### 12. What does `$P INIT` do?
Drains or stops a JES2 initiator.

### 13. What does `$C JOB jobname` do?
Cancels a job through JES2.

### 14. What does `$H J jobname` do?
Holds job output.

### 15. What does `$O J jobname` do?
Releases held job output.

### 16. What does `VARY device,ONLINE` do?
Makes a device available to MVS.

### 17. What does `MOUNT volume` do?
Makes a volume available on a device.

### 18. What does `D NET` show?
VTAM network status.

### 19. What is the SMP/E order?
RECEIVE, APPLY, then ACCEPT.

### 20. What does SMP/E RESTORE do?
Backs out an applied SYSMOD from the Target Zone.
