RECEIVERS="receiver1@mail.com receiver2@mail.com"
MAX_MAILS=3
HTTPS_URL="https://oriane.ink"
CURL_CMD="curl -I -s -o /dev/null -w %{http_code}"
CURL_MAX_CONNECTION_TIMEOUT="-m 30"

TLN_WATCHER_CNT=$(cat /root/tln_watcher.cnt)

CURL_RETURN_CODE=0
CURL_OUTPUT=`${CURL_CMD} ${CURL_MAX_CONNECTION_TIMEOUT} ${HTTPS_URL} 2> /dev/null` || CURL_RETURN_CODE=$?

if [ ${CURL_RETURN_CODE} -ne 0 ]; then
    if [ ${TLN_WATCHER_CNT} -lt ${MAX_MAILS} ]; then
        ((TLN_WATCHER_CNT++))
        echo "Échec cURL sur oriane.ink. Reboot secteur conseillé !" | \
            mail -s "Fail cURL oriane.ink" \
                 -a "From: TLN watcher <tln.watcher@gmail.com>" -a "Content-Type: text/plain; charset=UTF-8" \
                 ${RECEIVERS}
    fi
else
    if [ ${CURL_OUTPUT} -ne 200 ]; then
	if [ ${TLN_WATCHER_CNT} -lt ${MAX_MAILS} ]; then
            ((TLN_WATCHER_CNT++))
            echo "Anomalie HTTP sur oriane.ink (code ${CURL_OUTPUT}). Une intervention semble de mise." | \
                mail -s "Fail HTTP oriane.ink" \
                     -a "From: TLN watcher <tln.watcher@gmail.com>" -a "Content-Type: text/plain; charset=UTF-8" \
                     ${RECEIVERS}
        fi
    else
        TLN_WATCHER_CNT=0
    fi
fi

echo ${TLN_WATCHER_CNT} > /root/tln_watcher.cnt
