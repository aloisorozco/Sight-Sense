function add(n1: number | string, n2: number | string) {

    if (typeof n1 === 'number' && typeof n2 === 'number'){
        return n1 + n2;
    }
    return n1.toString() + n2.toString()
}

var person = {
    arr: ["sports", 1]
};
var arr;
arr = [];
// arr.push(1)
arr.push("str1");
for (var _i = 0, arr_1 = arr; _i < arr_1.length; _i++) {
    var i = arr_1[_i];
    console.log(i.toUpperCase());
}
var n1 = 5;
var n2 = 2.8;
var tuple;
tuple = [4, '4'];
tuple[0] = 55;
console.log(tuple);