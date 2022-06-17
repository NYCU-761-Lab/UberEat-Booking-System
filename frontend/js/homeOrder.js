$(document).ready(function() {
    const accessToken = sessionStorage.getItem("tokenStorage");
    let request_url = "http://127.0.0.1:8080";
    // global variables
    let shopName = null;
    let deliverType = null;
    let orderedProducts = [];
    let frontend_totalPrice = null;
    

    // edit the ordered products in the menu
    $(document).on('click', '.btn-add', async function(e) {  // add one product in menu
        let productName = e.target.id.slice(7);
        let currentCnt = $('#orderCnt_' + productName).val();
        $('#orderCnt_' + productName).val(Number(currentCnt) + 1);
        $('#orderCnt_' + productName).html(Number(currentCnt) + 1);
    });
    $(document).on('click', '.btn-minus', async function(e) {  // minus one product in menu
        let productName = e.target.id.slice(9);
        let currentCnt = $('#orderCnt_' + productName).val();
        $('#orderCnt_' + productName).val(Number(currentCnt) - 1);
        $('#orderCnt_' + productName).html(Number(currentCnt) - 1);
    });


    // click the "calculate Price" button
    $('.btn-calculatePrice').click(async function(e) {
        let subTotal = 0;
        let deliveryFee = 0;
        let totalPrice = 0;

        // get the order detail (shop name, deliver type, products...)
        shopName = e.target.id.slice(19);
        deliverType = $('#deliveryType').val();
        // get the products sold by the store
        let statusCode = null;
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'shop_name': shopName
        }
        let productList = await fetch(request_url + "/product/list", {
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
                return myJson['Product list of the shop'];
            }
        });
        // get the products in the order & calculate subTotal
        for (i in productList) {
            let productName = productList[i][0];
            let productNameNew = productName.replaceAll(" ", "---");

            let productPrice = productList[i][2];
            let productCnt = $('#orderCnt_' + productNameNew).val();
            // if (productCnt < 0) {
            //     alert("The order quality of the product is not positive integer.");
            // } else if (productCnt > 0) {
            //     orderedProducts.push({
            //         name:    productName,
            //         count:  productCnt,
            //         picture: productList[i][1],
            //         price: productPrice
            //     });
            //     subTotal  = subTotal + productCnt * productPrice;
            // }
            if (productCnt != 0) {  // 不論正負都會送POST
                orderedProducts.push({
                    name:    productName,
                    count:  productCnt,
                    picture: productList[i][1],
                    price: productPrice
                });
                subTotal  = subTotal + productCnt * productPrice;
            }
        } 


        // calculate delivery fee
        if (deliverType === "delivery") {
            body = {
                'shop_name': shopName
            }
            let distanceToShop = await fetch(request_url + "/shop/get_shop_distance", {
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
                    return myJson['Distance to the shop (km)'];
                }
            });
            deliveryFee = distanceToShop * 10;
            if (deliveryFee < 10) deliveryFee = 10;
            deliveryFee = Math.round(deliveryFee);  // 四捨五入

        } else if (deliverType === "pickup") {
            deliveryFee = 0;
        }


        // calculate all prices
        totalPrice = subTotal + deliveryFee;
        frontend_totalPrice = totalPrice;
        $('#subtotalPrice').text(subTotal);
        $('#deliveryPrice').text(deliveryFee);
        $('#totalPrice').text(totalPrice);


        // show the ordered products on the "calculated modal"
        $("#calculateModal").find('tbody').empty();
        for (i in orderedProducts) {
            // console.log(orderedProducts);
            $("#calculateModal").find('tbody')
            .append($('<tr>')
                .append($('<td>')
                    .append($('<img>')
                        .attr('src', orderedProducts[i].picture)
                        .attr('width', "100")
                        .attr('alt', orderedProducts[i].name)
                    )
                )
                .append($('<td>')
                    .text(orderedProducts[i].name)
                )
                .append($('<td>')
                    .text(orderedProducts[i].price)
                )
                .append($('<td>')
                    .text(orderedProducts[i].count)
                )
                .attr('class', 'orderedItems')
            );
        }
    });


    // click the Order button
    $('.btn-order').click(async function(e) {
        $("#calculateModal").find('tbody').empty();

        // get order details to use API
        let deliverType = $('#deliveryType').val();
        let orderDetails = [];
        for (i in orderedProducts) {
            orderDetails.push([orderedProducts[i].name, orderedProducts[i].count]);
        }

        // 不能送空包彈
        if (orderDetails.length > 0) {
            let statusCode = null;
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'order_shop_name': shopName,
                'order_details': orderDetails,
                'delivery_type': deliverType,
                'front_total_price': Number(frontend_totalPrice)
            }
            fetch(request_url + "/order/make", {
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
                if (statusCode === 200) {
                    alert(myJson['message']);
                    location.reload();  // refresh the page
                } else {
                    alert(myJson['message']);
                }
            });
        } else {
            alert("Your order cannot be completed! Please order something.");
        }
        orderedProducts = [];     
    });


    // click th close button
    $('.btn-close').click(function() {
        orderedProducts = [];
    });


    // recharge the wallet
    $('.btn-wallet').click(async function() {
        // let originalVal = Number($('#accountBalance').val());
        // let addValue = Number($('.walletVal').val());
        let originalVal = $('#accountBalance').val();
        let addValue = $('.walletVal').val();

        // $("#accountBalance").html(originalVal + addValue);
        // $("#accountBalance").val(originalVal + addValue);
        // $(".walletVal").val("");
        let statusCode = null;
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        let body = {
            'value': addValue
        }
        await fetch(request_url + "/auth/recharge", {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                alert(myJson['message']);
                location.reload();  // refresh the page
            } else {
                alert(myJson['message']);
            }
            $(".walletVal").val("");
        });
    });


    $('#homeItem').click(function() {
        window.location.reload();
    })
});