# MVS / TK5 Realtime Walkthrough

## Screens

- **MCS Console:** main operator command screen.
- **SDSF Jobs:** job queue view.
- **Job Output:** simulated JES2 job log.
- **Devices & Volumes:** hardware and dataset inventory.
- **IPL / System:** simulated IPL and system status.
- **SMP/E:** zone and SYSMOD status.

## Command groups

### Display commands
`D A,L`, `D A`, `D T`, `D M=DEV`, `D M=CHP`, `D VOLID`, `D ASM`, `D U`, `D XCF`, `D PARMLIB`

### Job control
`S proc`, `P proc`, `C job`, `F job,parameters`

### JES2 commands
`$DSPL`, `$DJ`, `$DJ(*)`, `$DI`, `$TI`, `$S INIT`, `$P INIT`, `$C JOB job`, `$H J job`, `$O J job`, `$T`

### Device and volume commands
`VARY dev,ONLINE`, `VARY dev,OFFLINE`, `MOUNT vol`, `UNMOUNT vol`

### VTAM commands
`D NET`, `D NET,MAJNODES`, `VARY NET,ACT,ID=node`, `VARY NET,INACT,ID=node`

### SMP/E commands
`SMPE RECEIVE`, `SMPE APPLY`, `SMPE ACCEPT`, `SMPE RESTORE`, `SMPE QUERY`

## Suggested practice

1. `D A,L`
2. `S START`
3. `D A,L`
4. `$DJ`
5. `F START,STATUS`
6. `P START`
7. `VARY 0581,OFFLINE`
8. `VARY 0581,ONLINE`
9. `D NET`
10. `SMPE RECEIVE`, `SMPE APPLY`, `SMPE ACCEPT`
11. `CLEAR`

## Safety

This is a browser simulation. It does not run real MVS code or affect a real z/OS system.
