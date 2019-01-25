# Kali customizations to the default shell environment

# Add /usr/local/sbin, /usr/sbin and /sbin to the PATH for all users
if ! echo "$PATH" | tr : '\n' | grep -q "^/sbin$"; then
    PATH="/usr/local/sbin:/usr/sbin:/sbin:$PATH"
fi
