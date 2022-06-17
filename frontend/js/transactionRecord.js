$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    let request_url = "http://127.0.0.1:8080";


    // every time click "transaction record", the result on the html DOM will be the newest
    $('#RecordItem').click(async function() {
        let actionType = $('#transactionType').val();
        getFinalList(actionType);
    })


    // after choosing the filter, show the newest result
    $('#transactionType').change(async function() {
        let actionType = $('#transactionType').val();
        getFinalList(actionType);
    })


    // different actions ('all' need to sort time)
    async function getFinalList(actionType) {
        let finalList = [];
        if (actionType === 'all') {
            // get each action's record
            let tmp1 = await getTransactionRecord('recharge');
            for (i in tmp1) {
                finalList.push(tmp1[i]);
            }
            let tmp2 = await getTransactionRecord('payment');
            for (i in tmp2) {
                finalList.push(tmp2[i]);
            }
            let tmp3 = await getTransactionRecord('receive');
            for (i in tmp3) {
                finalList.push(tmp3[i]);
            }

            // sort the record by the time
            finalList.sort(function(a, b) {
                let x = a[2];
                let y = b[2];
                if (x <= y) { return -1; }
                return 1;
            });
        } else {
            finalList = await getTransactionRecord(actionType);
        }
        showTransactionRecord(finalList);
    }


    // get the transaction result of a action (payment, receive, recharge)
    async function getTransactionRecord(action) {
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'req_type': action
        }
        let transactionList = await fetch(request_url + "/transaction/type_filter", { 
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['transaction_list'];
            }
        });
        return transactionList;
    }


    // show the transaction result with the list
    async function showTransactionRecord(transactionList) {
        // clear html DOM first
        $(".tranctionResult").find('tbody').empty();
        for (i in transactionList) {
            let transactionID = transactionList[i][0];
            let transactionType = transactionList[i][1];
            let transactionTime = transactionList[i][2];
            let transactionTrader = transactionList[i][3];
            let transactionMoney = transactionList[i][4];
            if (transactionType === "receive" || transactionType === "recharge") {
                transactionMoney = "+" + transactionMoney.toString();
            } else {
                transactionMoney = "-" + transactionMoney.toString();
            }

            // add elements to html DOM
            $(".tranctionResult").find('tbody')
            .append($('<tr>')
                .append($('<th>')
                    .text(Number(i) + 1)
                )
                .append($('<th>')
                    .attr('scope', 'row')
                    .text(transactionID)
                )
                .append($('<th>')
                    .attr('scope', 'row')
                    .text(transactionType)
                )
                .append($('<td>')
                    .text(transactionTime)
                )
                .append($('<td>')
                    .text(transactionTrader)
                )
                .append($('<td>')
                    .text(transactionMoney)
                )
            );
        }
    }
});