$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    let request_url = "http://127.0.0.1:8080";
    let checkItems = [];  // 哪些 checkbox 有被選起來


    // every time click "my order", the result on the html DOM will be the newest
    $('#myOrderItem').click(async function() {
        getFinalList();
    })


    // after choosing the filter, show the newest result
    $('#myOrderType').change(async function() {
        getFinalList();
    })


    // different actions ('all' need to sort the time)
    async function getFinalList() {
        let actionType = $('#myOrderType').val();
        let finalList = [];
        if (actionType === 'all') {
            // get each action's record
            let tmp1 = await getMyOrderList('Finished');
            for (i in tmp1) {
                finalList.push(tmp1[i]);
            }
            let tmp2 = await getMyOrderList('Not Finish');
            for (i in tmp2) {
                finalList.push(tmp2[i]);
            }
            let tmp3 = await getMyOrderList('Cancel');
            for (i in tmp3) {
                finalList.push(tmp3[i]);
            }

            // sort the record by the time
            finalList.sort(function(a, b) {
                let x = a[0].toLowerCase();
                let y = b[0].toLowerCase();
                if (x < y) { return 1; }
                // if (x < y) { return -1; }
                return 0;
            });
        } else {
            finalList = await getMyOrderList(actionType);
        }
        // console.log(finalList);
        showMyOrderList(finalList);
    }


    // get the transaction result of a action (finished, not finished, cancel)
    async function getMyOrderList(action) {
        let statusCode = null;
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'req_status': action
        }
        let myOrderList = await fetch(request_url + "/order/user_filter", { 
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            // console.log(response);
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['my_order_list'];
            }
        });
        return myOrderList;
    }


    // show my order result with the list
    async function showMyOrderList(myOrderList) {
        // clear html DOM first
        $(".myOrderResult").find('tbody').empty();
        for (i in myOrderList) {
            let myOrderID = myOrderList[i][0];
            let myOrderStatus = myOrderList[i][1];
            let myOrderStartTime = myOrderList[i][2];
            let myOrderEndTime = myOrderList[i][3];
            let myOrderShopName = myOrderList[i][4];
            let myOrderPrice = myOrderList[i][5];
            let myOrderAction = myOrderList[i][6];  // a list, if "cancel" is in the list, means that it can do the cancel action

            // add elements to html DOM
            if (myOrderAction.includes('cancel')) {   // add cancel button if this order can be canceled
                $(".myOrderResult").find('tbody')
                .append($('<tr>')
                    .append($('<th>')  // checkbox
                        .append($('<input type="checkbox">')
                            .attr('id', 'check_' + myOrderID)
                            .attr('class', 'myOrder_checkbox')
                            .attr('value', 'check_' + myOrderID)
                        )
                    )
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(myOrderID)
                    )
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(myOrderStatus)
                    )
                    .append($('<td>')
                        .text(myOrderStartTime)
                    )
                    .append($('<td>')
                        .text(myOrderEndTime)
                    )
                    .append($('<td>')
                        .text(myOrderShopName)
                    )
                    .append($('<td>')
                        .text(myOrderPrice)
                    )
                    .append($('<td>')  // order details button
                        .append($('<button>')
                            .attr('type', 'button')
                            .attr('class', 'btn btn-info btn-orderDetail')
                            .attr('id', 'orderDetailBtn_' + myOrderID + '_shopName_' + myOrderShopName)
                            .attr('data-toggle', 'modal')
                            .attr('data-target', '#orderDetailModal')
                            .text('order details')
                        )
                    )
                    .append($('<td>')  // cancel button
                        .append($('<button>')
                            .attr('type', 'button')
                            .attr('class', 'btn btn-danger btn-cancel')
                            .attr('id', 'cancelBtn_' + myOrderID)
                            .text('Cancel')
                        )
                    )
                );
            } else {
                $(".myOrderResult").find('tbody')
                .append($('<tr>')
                    .append($('<th>'))  // no checkbox
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(myOrderID)
                    )
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(myOrderStatus)
                    )
                    .append($('<td>')
                        .text(myOrderStartTime)
                    )
                    .append($('<td>')
                        .text(myOrderEndTime)
                    )
                    .append($('<td>')
                        .text(myOrderShopName)
                    )
                    .append($('<td>')
                        .text(myOrderPrice)
                    )
                    .append($('<td>')  // order details button
                        .append($('<button>')
                            .attr('type', 'button')
                            .attr('class', 'btn btn-info btn-orderDetail')
                            .attr('id', 'orderDetailBtn_' + myOrderID + '_shopName_' + myOrderShopName)
                            .attr('data-toggle', 'modal')
                            .attr('data-target', '#orderDetailModal')
                            .text('order details')
                        )
                    )
                );
            }
        }
    }


    // Press "order details" button
    $(document).on('click', '.btn-orderDetail', async function(e) {
        // get the order ID and the from id
        let tmpIdx = e.target.id.search('_shopName_');
        let orderID = e.target.id.slice(15, tmpIdx);
        let orderShopName = e.target.id.slice(tmpIdx + 10);
        let orderList = null;
        let orderPrice = null;

        let statusCode = null;
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'shop_name': orderShopName,
            'order_id': orderID
        }
        await fetch(request_url + "/order/detail", { 
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            // console.log(response);
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                orderList =  myJson['order_item_detail'];
                orderPrice = myJson['order_price_list'];
            }
        });
        // add products to html DOM
        $(".orderDetailTable").find('tbody').empty();
        for (i in orderList) {
            let productImg = orderList[i][0];
            let productName = orderList[i][1];
            let productPrice = orderList[i][2];
            let productQuantity = orderList[i][3];

            $(".orderDetailTable").find('tbody')
            .append($('<tr>')
                .append($('<td>')
                    .append($('<img>')
                        .attr('src', productImg)
                        .attr('width', "100")
                        .attr('src', productImg)
                        .attr('alt', productName)
                    )
                )
                .append($('<td>')
                    .text(productName)
                )
                .append($('<td>')
                    .text(productPrice)
                )
                .append($('<td>')
                    .text(productQuantity)
                )
            );
        }
        // 顯示外送費用
        $('#order_subtotal').text(orderPrice[0]);
        $('#order_deliveryFee').text(orderPrice[1]);
        $('#order_totalPrice').text(orderPrice[2]);
    });


    // Press "Cancel" button
    $(document).on('click', '.btn-cancel', async function(e) { 
        let statusCode = null;
        // delete the product
        let orderID = e.target.id.slice(10);
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'order_id': orderID
        }
        fetch(request_url + "/order/user_cancel", {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            console.log(response);
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            console.log(myJson);
            if (statusCode === 200) {
                alert(myJson['message']);
                getFinalList();  // 刷新列表
            } else {
                alert(myJson['message']);
            }
        });
    });


    // Bonus
    // 把勾起來的 checkbox 加到 checkItems 裏面
    $(document).on('change', '.myOrder_checkbox', function(e) {
        let itemID = e.target.id.slice(6);
        if(e.target.checked) {
            if (checkItems.includes(itemID) === false) {  // 避免重複加到 list
                checkItems.push(itemID);
            }
        } else {
            const idx = checkItems.indexOf(itemID);
            if (idx > -1) {
                checkItems.splice(idx, 1);
            }
        }
    });

    // cancel these items
    $('#myOrder-cancels-btn').click(async function() {
        console.log(checkItems);
        for (orderID in checkItems) {
            let statusCode = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'order_id': orderID
            }
            fetch(request_url + "/order/user_cancel", {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                console.log(response);
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                console.log(myJson);
                if (statusCode === 200) {
                    alert(myJson['message']);
                    getFinalList();  // 刷新列表
                } else {
                    alert(myJson['message']);
                }
            });
        }
    })
});