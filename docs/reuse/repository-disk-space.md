As of April 2026, these are the estimates for the amount of disk space needed to download the following Ubuntu distributions:

| Series | amd64 | i386  | Both |
| ------ | ----- | ----- | ----- |
| Resolute | 150GB | 110GB | 180GB |
| Noble  | 625GB | 170GB | 680GB |
| Jammy  | 945GB | 140GB | 975GB |
| Focal  | 655GB | 115GB | 670GB |
| Bionic | 335GB | 155GB | 395GB |

Packages will be downloaded to `/var/lib/landscape/landscape-repository/standalone/`. These estimates are a breakdown of the total size of the pockets for the main, restricted, universe, and multiverse components of the amd64 and i386 architectures (release, updates and security pockets). The last column provides an estimate for downloading both the amd64 and i386 architectures. It's not a total of the amd64 and i386 disk space requirements because it doesn't duplicate packages that are present in both architectures.

These estimates are only a subset, and it doesn't include arm and other architectures. Including these will use more disk space.

Note that the [restricted component](https://help.ubuntu.com/community/Repositories#Restricted) is usually large, and it contains proprietary packages and drivers that aren't fully open-source (e.g., Nvidia graphics drivers). If you know you won't need these packages and drivers, you could significantly reduce the size of your mirrors by not mirroring the restricted component.