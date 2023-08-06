#!/bin/bash

if [ -z "$1" ]; then
    echo 'No target provided !'
    echo "Usage: ./$0 target [domain username password]"
    exit 1
fi

if [ -z "$2" ]; then
    domain="."
else
    domain=$2
fi
if [ -n "$3" ]; then
    username=$3
fi
if [ -n "$4" ]; then
    password=$4
fi

if [ -z "$password" ]; then
    username="randomlolmdr"

    cd /opt/CrackMapExec
    echo "$ cme smb $1" 
    poetry run cme smb "$1" 2>/dev/null
    
    
    echo "$ cme smb $1 -u '' -p '' --shares" 
    poetry run cme smb "$1" -u '' -p '' --shares 2>/dev/null
    
    echo "$ cme smb $1 -u $username -p '' --shares" 
    poetry run cme smb "$1" -u $username -p '' --shares 2>/dev/null
    cd -
    
    echo
    echo "$ smbclient -L //$1/ -U '%'"
    smbclient -L "//$1/" -U '%'
    
    echo
    echo "$ smbclient -L //$1/ -U '$username%'"
    smbclient -L "//$1/" -U '$username%'
    
    # echo
    # echo "msf> auxiliary/scanner/smb/smb_version"
    # msfconsole -q -x "use auxiliary/scanner/smb/smb_version; set RHOSTS $1; run; exit"
    
    #echo
    #echo "msf> auxiliary/scanner/smb/smb_ms17_010"
    #msfconsole -q -x "use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS $1; run; exit"
    
    #echo 
    #echo "msf> auxiliary/scanner/smb/smb_enumshares"
    #msfconsole -q -x "use auxiliary/scanner/smb/smb_enumshares; set RHOSTS $1; run; set SMBUser $username; run; exit"
    
    echo
    echo "nmap -sVC -p 139,445 -Pn '--script=smb-vuln-*' $1"
    #nmap -p 139,445 -Pn --script=smb-vuln-cve2009-3103.nse,smb-vuln-ms06-025.nse,smb-vuln-ms07-029.nse,smb-vuln-ms08-067.nse,smb-vuln-ms10-054.nse,smb-vuln-ms10-061.nse,smb-vuln-ms17-010.nse $1
    nmap -sVC -p 139,445 -Pn '--script=smb-vuln-*' $1
    
    echo
    echo "$ enum4linux-ng '$1' -A -R"
    enum4linux-ng "$1" -A -R 
    
    echo
    echo "$ enum4linux-ng '$1' -A -R -u '$username' -p ''"
    enum4linux-ng "$1" -A -R -u "$username" -p ''
else
    cd /opt/CrackMapExec
    echo "$ cme smb $1 -d '$domain' -u '$username' -p '$password' --shares" 
    poetry run cme smb "$1" -d "$domain" -u "$username" -p "$password" --shares 2>/dev/null
    cd -
    
    echo
    echo "$ smbclient -L //$1/ -U '$domain\\username%$password'"
    smbclient -L "//$1/" -U "$domain\\$username%$password"
    
    # echo
    # echo "msf> auxiliary/scanner/smb/smb_version"
    # msfconsole -q -x "use auxiliary/scanner/smb/smb_version; set RHOSTS $1; run; exit"
    
    #echo
    #echo "msf> auxiliary/scanner/smb/smb_ms17_010"
    #msfconsole -q -x "use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS $1; run; exit"
    
    #echo 
    #echo "msf> auxiliary/scanner/smb/smb_enumshares"
    #msfconsole -q -x "use auxiliary/scanner/smb/smb_enumshares; set RHOSTS $1; run; set SMBUser $username; run; exit"
    
    echo
    echo "nmap -sVC -p 139,445 -Pn '--script=smb-vuln-*' $1"
    #nmap -p 139,445 -Pn --script=smb-vuln-cve2009-3103.nse,smb-vuln-ms06-025.nse,smb-vuln-ms07-029.nse,smb-vuln-ms08-067.nse,smb-vuln-ms10-054.nse,smb-vuln-ms10-061.nse,smb-vuln-ms17-010.nse $1
    nmap -sVC -p 139,445 -Pn '--script=smb-vuln-*' $1
    
    echo
    echo "$ enum4linux-ng '$1' -A -R -w '$domain' -u '$username' -p ''"
    enum4linux-ng "$1" -A -R -w $domain -u "$username" -p "$password"
fi
