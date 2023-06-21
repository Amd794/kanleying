const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
XMLHttpRequest = window.XMLHttpRequest

var _keyStr =
        //
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    //
;
function _utf8_decode(c) {
  for (var a = "", b = 0, d = 0, c2, c3; b < c.length;) {
    d = c.charCodeAt(b);
    if (128 > d) {
      a += String.fromCharCode(d);
      b++
    } else if (191 < d && 224 > d) {
      c2 = c.charCodeAt(b + 1);
      a += String.fromCharCode((d & 31) << 6 | c2 & 63);
      b += 2
    } else {
      c2 = c.charCodeAt(b + 1);
      c3 = c.charCodeAt(b + 2);
      a += String.fromCharCode((d & 15) << 12
          | (c2 & 63) << 6 | c3 & 63);
      b += 3;
    }
  }
  return a
}
function decode(c) {
  var a = "", b, d, h, f, g, e = 0;
  c = c.replace(/[^A-Za-z0-9\+\/\=]/g, "");
  for (; e < c.length;) {
    b = _keyStr.indexOf(c.charAt(e++));
    d = _keyStr.indexOf(c.charAt(e++));
    f = _keyStr.indexOf(c.charAt(e++));
    g = _keyStr.indexOf(c.charAt(e++));
    b = b << 2 | d >> 4;
    d = (d & 15) << 4 | f >> 2;
    h = (f & 3) << 6 | g;
    a += String.fromCharCode(b);
    64 != f && (a += String.fromCharCode(d));
    64 != g && (a += String.fromCharCode(h));
  }
  return  _utf8_decode(a)
}
function getArr(T, N){
  var N = eval(N)
  var len, locate, str;
  T = T.split('');
  N = N.match(/\d+[a-zA-Z]+/g);
  // console.log(N);
  len = N.length;
  while (len--) {
    locate = parseInt(N[len]) & 255;
    str = N[len].replace(/\d+/g, '');
    T.splice(locate, str.length)
  }
  T = T.join('');
  // console.log(JSON.parse(decode(T)))
  return JSON.parse(decode(T))
}

// let T = "afeyeJjb2dde1epYyI6eyJpZCI6NjUxMjYzLCJ0aXRsZSI6Ilx1NjIxMVx1NTcaayOFx1NWYwMlx1NzU0Y1x1adNWY1M1x1NjU1OVx1NzIzNiIsImacNvbGxlY3QiOiIyNTMyNjgiLCJpc0phcGFuQ29taWMiOmZhbHNlLCJpc0xpZ2h0Tm92ZWwiOmZhbHNlLCJpc0xpZ2h0Q29taWMiOmZhbHNlLCJpc0ZpbmlzaCI6ZmFsc2UsImlzUm9hc3RhYmxlIjp0cnVlLCJlSWQiOiJLbEJNVDB0R1hWRmJDQU1mQWdBSEJRNEtIRUpjV2swcyJ9LCJjaGFwdGVyIjp7ImNpZCI6MjMzOCwiY1RpdGxlIjoiNjYwLVx1NTNiYlx1NWI4Y1x1NjIxMFx1ODFlYVx1NWRmMVx1NzY4NFx1NWE1YVx1NzkzY1x1NTQyNyIsInZpcFN0YXR1cyI6Miwidl9jbHViX3N0YXRlIjoxLCJpc19hcHBfY2hhcHRlciI6MCwiY1NlcSI6IjY2MCIsInByZXZDaWQiOjIzMzMsIm5leHRDaWQiOjAsImJsYW5rRmlyc3QiOjEsImNhblJlYWQiOmZhbHNlfSwicGljdHVyZSI6W3sicGlkIjoiMzU3ODUiLCJ3aWR0aCI6MTIwMCwiaGVpZ2h0IjozMDAwLCJ1cmwiOiJodHRwczpcL1wvbWFuaHVhLmFjaW1nLmNuXC9tYW5odWFfZGV0YWlsXC8wXC8wN18xN180MF9hYTA0OTgzMjUzYWI4ZTA0ZWI4MTAxOWUxMTc3NDVhZjdfMTI1MzE4NTE0LmpwZ1wvMCJ9XSwiYWRzIjp7InRvcCI6IiIsImJvdHRvbSI6IiJ9LCJhcnRpc3QiOnsiYXZhdGFyIjoiaHR0cHM6XC9cL1wvdGhpcmRxcS5xbG9nby5jblwvZz9iPW9pZGImaz1zYkhJRzVnWG4zVVdKRklqUDRneGZ3JnM9MTAwJnQ9MTYzNzg5ODEzMyIsIm5pY2siOiJcdTUyMWJcdThmZjlcdTY1ODdcdTUzMTYiLCJ1aW5DcnlwdCI6IlIwbGhVV0pOUWpObGEwNVJNMlUwTDIxVFoyTmhVVDA5In19"
// let N = `"c55aa7e1" + (+eval("0 * 0")).toString() + "5ac6dde8" + (+eval("5&5")).toString() + "869906ad2e0af4"`
//
// console.log(getArr(T, N));