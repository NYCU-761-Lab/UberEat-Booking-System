// encode base64 image using javascript
let encodeImage = null;
// let hasImage = false;
function encodeImageFileAsURL(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        encodeImage = reader.result;
    }
    reader.readAsDataURL(file);
    // hasImage = true;
}

$(document).ready(function() {
    const accessToken = localStorage.getItem("tokenStorage");
    let request_url = "http://127.0.0.1:8080";
    // Due to security, javascript will not show the full path of the image
    let image_path = "/Users/angelahsi/Desktop/NYCU/大二下課程/資料庫/HW2/UberEat-Booking-System/backend/product_image/";

    // every time we do some modify, refresh the list
    async function refreshProductList(shopName) {
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
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
                // console.log(myJson['Product list of the shop']);
                return myJson['Product list of the shop'];
            }
        });

        // clear html DOM first
        $(".shopProductResult").find('tbody').empty();
        for (i in productList) {
            let productName = productList[i][0];
            let productImg = productList[i][1];
            let productPrice = productList[i][2];
            let productQuantity = productList[i][3];

            // add elements to html DOM
            $(".shopProductResult").find('tbody')
            .append($('<tr>')
                .append($('<th>')
                    .attr('scope', 'row')
                    .text(Number(i) + 1)
                )
                .append($('<td>')
                    .append($('<img>')
                        .attr('src', productImg)
                        .attr('width', "180")
                        // .attr('height', "10")
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
                .append($('<td>')
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-info')
                        .attr('data-toggle', 'modal')
                        .attr('data-target', '#' + productName)
                        .text('Edit')
                    )
                )
                // .append($('<div>')  // modal
                //     .attr('class', 'modal fade')
                //     .attr('id', productName)
                //     .attr('data-backdrop', 'static')
                //     .attr('tabindex', '-1')
                //     .attr('role', 'dialog')
                //     .attr('aria-labelledby' ,'staticBackdropLabel')
                //     .attr('aria-hidden', 'true')
                //     .append($('div')
                //         .attr('class', 'modal-dialog')
                //         .attr('role', 'document')
                //         .append($('<div>')
                //             .attr('class', 'modal-content')
                //             .append($('<div>')
                //                 .attr('class', 'modal-header')
                //                 .append($('<h5>')
                //                     .attr('class', 'modal-title')
                //                     .attr('id', 'staticBackdropLabel')
                //                     .text(productName + 'edit')
                //                 )
                //                 .append($('<button>')
                //                     .attr('type', 'button')
                //                     .attr('class', 'close')
                //                     .attr('data-dismiss', 'modal')
                //                     .attr('aria-label', 'Close')
                //                     .append($('<span>')
                //                         .attr('aria-hidden', 'true')
                //                         .text('&times;')
                //                     )
                //                 )
                //             )
                //             .append($('<div>')
                //                 .attr('class', 'modal-body')
                //                 .append($('<div>')
                //                     .attr('class', 'row')
                //                     .append($('<div>')
                //                         .attr('class', 'col-xs-6')
                //                         .append($('<label>')
                //                             .attr('for', 'ex72')
                //                             .text('price')
                //                         )
                //                         .append($('<input>')
                //                             .attr('class', 'form-control')
                //                             .attr('id', 'ex72')
                //                             .attr('type', 'text')
                //                         )
                //                     )
                //                     .append($('<div>')
                //                         .attr('class', 'col-xs-6')
                //                         .append($('<label>')
                //                             .attr('for', 'ex42')
                //                             .text('quantity')
                //                         )
                //                         .append($('<input>')
                //                             .attr('class', 'form-control')
                //                             .attr('id', 'ex42')
                //                             .attr('type', 'text')
                //                         )
                //                     )
                //                 )
                //             )
                //             .append($('<div>')
                //                 .attr('class', 'modal-footer')
                //                 .append($('<button>')
                //                     .attr('type', 'button')
                //                     .attr('class', 'btn btn-secondary')
                //                     .attr('data-dismiss', 'modal')
                //                     .text('Edit')
                //                 )
                //             )
                //         )
                //     )
                // )
                .append($('<td>')
                    .append($('<button>')
                        .attr('type', 'button')
                        .attr('class', 'btn btn-danger')
                        .text('Delete')
                    )
                )
            );
        }
    }

    $("#shopItem").click(async function() {
        let statusCode = null;
        let shopName = null;
        
        // Get shop's name
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        shopName = await fetch(request_url + "/shop/get_shop_name_of_user", {
            method: 'POST',
            headers: headers
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['shop_name of the user'];
            }
        });

        // 使用者沒有商店的情況會有後端擋掉，記得判斷
        if (shopName != null) {
            // show current products
            refreshProductList(shopName);
        }
    });

    // add new product
    $(".addProductBtn").click(async function() {
        let shopName = null;
        let addMeal = $(".addMeal").val();
        let addPrice = $(".addPrice").val();
        let addQuantity = $(".addQuantity").val();
        let addImage = encodeImage;
        
        // Get shop's name
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + accessToken
        }
        shopName = await fetch(request_url + "/shop/get_shop_name_of_user", {
            method: 'POST',
            headers: headers
        })
        .then(function(response) {
            statusCode = response['status'];
            return response.json();
        })
        .then(function(myJson) {
            if (statusCode === 200) {
                return myJson['shop_name of the user'];
            }
        });

        // add the product
        if (addMeal === "" || addPrice === "" || addQuantity === "") {
            alert("The field cannot be left blank.");
        } else {
            let headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + accessToken
            }
            let body = {
                'product_name': addMeal,
                'price': addPrice,
                'quantity': addQuantity,
                'picture': addImage
            }

            let statusCode = null;
            fetch(request_url + "/product/register", {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(function(response) {
                statusCode = response['status'];
                return response.json();
            })
            .then(function(myJson) {
                console.log(myJson);
                if (statusCode === 200) {
                    alert(myJson['message']);
                    refreshProductList(shopName);
                } else {
                    alert(myJson['message']);
                }
            });
        }
        encodeImage = null;  // refresh
        // hasImage = false;  // refresh
    });

    // edit current product


    // delete current product
});