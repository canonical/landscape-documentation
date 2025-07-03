(how-to-external-auth-pam)=
# How to enable PAM authentication

If you want to use Pluggable Authentication Modules (PAM) to authenticate users in your self-hosted Landscape server, you must create the file `/etc/pam.d/landscape` with the appropriate PAM configuration.

The simplest possible file is:
```
#%PAM-1.0
auth required pam_ldap.so
account required pam_ldap.so
```

Once these are in place, restart Landscape Server and it should be possible to login to the Landscape dashboard with your NID credentials. Additional administrators can be added via email.

If you use PAM to authenticate, the user details stored in Landscape are associated with the PAM identity supplied. PAM authentication has been tested against an LDAP server running on Ubuntu, and also with Active Directory running on Windows.

For more information on PAM authentication see [PAM Tutorial](https://wpollock.com/AUnix2/PAM-Help.htm).

