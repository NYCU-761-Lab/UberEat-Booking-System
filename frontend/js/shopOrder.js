$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    let request_url = "http://127.0.0.1:8080";
    let checkItems = [];  // 哪些 checkbox 有被選起來

    // every time click "shop order", the result on the html DOM will be the newest
    $('#shopOrderItem').click(async function() {
        getFinalList();
    })


    // after choosing the filter, show the newest result
    $('#shopOrderType').change(async function() {
        getFinalList();
    })


    // different actions ('all' need to sort the time)
    async function getFinalList() {
        let actionType = $('#shopOrderType').val();
        let finalList = [];
        if (actionType === 'all') {
            // get each action's record
            let tmp1 = await getShopOrderList('Finished');
            for (i in tmp1) {
                finalList.push(tmp1[i]);
            }
            let tmp2 = await getShopOrderList('Not Finish');
            for (i in tmp2) {
                finalList.push(tmp2[i]);
            }
            let tmp3 = await getShopOrderList('Cancel');
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
            finalList = await getShopOrderList(actionType);
        }
        // console.log(finalList);
        showShopOrderList(finalList);
    }


    // get the transaction result of a action (finished, not finished, cancel)
    async function getShopOrderList(action) {
        // Get shop's name
        // let shopName = getShopName();

        // get order list of the shop
        let statusCode = null;
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            // 'shop_name': shopName,
            'req_status': action
        }
        let shopOrderList = await fetch(request_url + "/order/shop_filter", { 
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
                return myJson['shop_order_list'];
            }
        });
        return shopOrderList;
    }


    // show shop order result with the list
    async function showShopOrderList(shopOrderList) {
        // clear html DOM first
        $(".shopOrderResult").find('tbody').empty();
        for (i in shopOrderList) {
            let shopOrderID = shopOrderList[i][0];
            let shopOrderStatus = shopOrderList[i][1];
            let shopOrderStartTime = shopOrderList[i][2];
            let shopOrderEndTime = shopOrderList[i][3];
            let shopOrderShopName = shopOrderList[i][4];
            let shopOrderPrice = shopOrderList[i][5];
            let shopOrderAction = shopOrderList[i][6];  // a list, if "cancel" is in the list, means that it can do the cancel action

            // add elements to html DOM
            if (shopOrderAction.includes('cancel') && shopOrderAction.includes('done')) {   // add cancel button if this order can be canceled
                $(".shopOrderResult").find('tbody')
                .append($('<tr>')
                    .append($('<th>')  // checkbox
                        .append($('<input type="checkbox">')
                            .attr('id', 'check_' + shopOrderID)
                            .attr('class', 'shopOrder_checkbox')
                            .attr('value', 'check_' + shopOrderID)
                        )
                    )
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(shopOrderID)
                    )
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(shopOrderStatus)
                    )
                    .append($('<td>')
                        .text(shopOrderStartTime)
                    )
                    .append($('<td>')
                        .text(shopOrderEndTime)
                    )
                    .append($('<td>')
                        .text(shopOrderShopName)
                    )
                    .append($('<td>')
                        .text(shopOrderPrice)
                    )
                    .append($('<td>')  // order details button
                        .append($('<button>')
                            .attr('type', 'button')
                            .attr('class', 'btn btn-info btn-orderDetail')
                            .attr('id', 'orderDetailBtn_' + shopOrderID + '_shopName_' + shopOrderShopName)
                            .attr('data-toggle', 'modal')
                            .attr('data-target', '#shopOrderDetailModal')
                            .text('order details')
                        )
                    )
                    .append($('<td>')  
                        .append($('<button>')  // done button
                            .attr('type', 'button')
                            .attr('class', 'btn btn-done btn-success')
                            .attr('id', 'doneBtn_' + shopOrderID)
                            .attr('style', 'margin-right:5px;')
                            .text('Done')
                        )
                        .append($('<button>')  // cancel button
                            .attr('type', 'button')
                            .attr('class', 'btn btn-danger btn-cancel-shop')
                            .attr('id', 'cancelBtn_' + shopOrderID)
                            .text('Cancel')
                        )
                    )
                );
            } else {
                $(".shopOrderResult").find('tbody')
                .append($('<tr>')
                    .append($('<th>'))  // no checkbox
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(shopOrderID)
                    )
                    .append($('<th>')
                        .attr('scope', 'row')
                        .text(shopOrderStatus)
                    )
                    .append($('<td>')
                        .text(shopOrderStartTime)
                    )
                    .append($('<td>')
                        .text(shopOrderEndTime)
                    )
                    .append($('<td>')
                        .text(shopOrderShopName)
                    )
                    .append($('<td>')
                        .text(shopOrderPrice)
                    )
                    .append($('<td>')  // order details button
                        .append($('<button>')
                            .attr('type', 'button')
                            .attr('class', 'btn btn-info btn-orderDetail')
                            .attr('id', 'orderDetailBtn_' + shopOrderID + '_shopName_' + shopOrderShopName)
                            .attr('data-toggle', 'modal')
                            .attr('data-target', '#shopOrderDetailModal')
                            .text('order details')
                        )
                    )
                );
            }
        }
    }


    // Press "order details" button, same as the one in myOrder.js
    $(document).on('click', '.btn-orderDetail', async function(e) {
        // get the order ID and the from id
        let tmpIdx = e.target.id.search('_shopName_');
        let orderID = e.target.id.slice(15, tmpIdx);
        // let orderShopName = e.target.id.slice(tmpIdx + 10);
        let orderList = null;
        let orderPrice = null;
        console.log(orderID);

        let statusCode = null;
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            // 'shop_name': orderShopName,
            'order_id': orderID
        }
        await fetch(request_url + "/order/detail", { 
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
                orderList =  myJson['order_item_detail'];
                orderPrice = myJson['order_price_list'];
            }
        });
        // add products to html DOM
        $(".shopOrderDetailTable").find('tbody').empty();
        for (i in orderList) {
            let productImg = orderList[i][0];
            let productName = orderList[i][1];
            let productPrice = orderList[i][2];
            let productQuantity = orderList[i][3];

            $(".shopOrderDetailTable").find('tbody')
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
        $('#shopOrder_subtotal').text(orderPrice[0]);
        $('#sopOrder_deliveryFee').text(orderPrice[1]);
        $('#shopOrder_totalPrice').text(orderPrice[2]);
    });


    // Press "Done" button
    $(document).on('click', '.btn-done', async function(e) {
        // Get shop's name
        let shopName = getShopName();

        // complete the order
        let statusCode = null;
        let orderID = e.target.id.slice(8);
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'shop_name': shopName,
            'order_id': orderID
        }
        fetch(request_url + "order/shop_complete", {
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


    // Press "Cancel" button
    $(document).on('click', '.btn-cancel-shop', async function(e) { 
        // Get shop's name
        let shopName = getShopName();

        // cancel the order of the shop
        let statusCode = null;
        let orderID = e.target.id.slice(10);
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'shop_name': shopName,
            'order_id': orderID
        }
        fetch(request_url + "/order/shop_cancel", {
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
    $(document).on('change', '.shopOrder_checkbox', function(e) {
        let itemID = e.target.id.slice(7);
        console.log(itemID);
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


    // finish these items
    $('#shopOrder-dones-btn').click(async function() {
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
            fetch(request_url + "/order/shop_complete", {
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
    });


    // cancel these items
    $('#shopOrder-cancels-btn').click(async function() {
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
            fetch(request_url + "/order/shop_cancel", {
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
    });

});