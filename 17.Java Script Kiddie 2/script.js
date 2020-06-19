const fetch = require("node-fetch"); // Install node-fetch to be able to use fetch api

(async function(){
  let bytes;
  try{
   var res = await fetch("https://2019shell1.picoctf.com/problem/12281/bytes",{method:"GET"});
   var body = await res.text()
   bytes =  body.split(" ").map(x => Number(x));
//   console.log(bytes.length)
  }catch(e){
    console.log("error",e);
  }
var png_signature = [137,80,78,71,13,10,26,10];//hex to decimal results  
var ihdr = [0,0,0,13,73,72,68,82]
var possible_val = generate_poss_values([...png_signature,...ihdr],bytes)
loop(gen_keys(possible_val))
})()

function gen_idx(arr,bytes){// generate indexes for known (png signature,IHDR) values of png inside of bytes array , to know at what index position they are located .
 let idx = [];
for(let x in arr){
    var obj = {}
    obj[arr[x]] = []
  for(let j in bytes){
    if(bytes[j] === arr[x]){
      obj[arr[x]].push(j)
    }
  }
  idx.push(obj)
}
return idx
}

function generate_poss_values(arr,bytes){
  var indexes = gen_idx([...arr],bytes)
  var indexes_len = indexes.length;
  let obj = {}
  let png_ihdr = [...arr].map(x => String(x)) // so i can have object keys as strings 
  for(var i = 0;i < indexes_len;i++){
    let valz = indexes[i][png_ihdr[i]];
    for(let j in valz){
      let n = Number(valz[j])
      let calc = ((n-i)/16)
      if(Number.isInteger(calc) && String(calc).length === 1){ // no float 1.x 
        var chr = png_ihdr[i] + '-' + 'key_position-' + i; // + inc
        obj[chr] = obj.hasOwnProperty(chr) && obj[chr].length > 0 ? [...obj[chr],calc] : [calc];
      }
    }
  }
// console.log("object with index key position in bytes array",obj) //
  
 return obj
}

function gen_keys(obj){
  var keys = []
  for(let[,v] of Object.entries(obj)){
    if(v.length > 1){
      v = v.map( n => String(n))
      keys.push(v)
    }else{
      v[0] = String(v[0])
      keys.push(v[0])
    }
  } 
  return keys
}

function loop(arr,curr=""){
 if(Array.isArray(arr) && arr.length === 0){
   curr = curr.split("").join("0") + "0" // every odd should be a number that we care about , even doesn't matter it is just to fill length of 32 for key
   console.log("possible key : ",curr)
   return
 }
 var el = arr[0]
 if(typeof(el) == 'string'){

   loop(arr.slice(1),curr + el)
 }else {

   for(let i in el){
     loop(arr.slice(1),curr + el[i])
   }
 }
}
