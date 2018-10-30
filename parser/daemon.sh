# inotifywait -q -m -e close_write /var/mail/recipient |
# while read -r filename event; do
#   echo "changed"         # or "./$filename"
#   cp /var/mail/recipient /tmp/var_mail_recipient
#   echo " " > /var/mail/recipient
#   echo $(read -r filename event;)
# done

# while true
# do 
#     echo "Hi"
#     sleep 1
# done

tail -f /var/mail/* | formail -k -X X-Original-To: -X From: -X Subject: -ds sh -c 'cat > /data/emails/mail.$FILENO.mail' &
python3 parse.py