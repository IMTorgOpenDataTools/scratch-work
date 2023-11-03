
// ProcessData
export function addDays(date, days){
    //Add n(int) days to a Date and return new Date
    let resultDate = new Date( JSON.parse(JSON.stringify(date)) )
    resultDate.setDate(date.getDate() + days)
    return resultDate
  }
  
  
  export function randomIntFromInverval(min, max){
    //Get random integer between two integers
    return Math.floor(Math.random() * (max - min + 1) + min)
  }
  
  export function groupBy(list, keyGetter) {
    /**
     * @description
     * Takes an Array<V>, and a grouping function,
     * and returns a Map of the array grouped by the grouping function.
     *
     * @param list An array of type V.
     * @param keyGetter A Function that takes the the Array type V as an input, and returns a value of type K.
     *                  K is generally intended to be a property key of V.
     *
     * @returns Map of the array grouped by the grouping function.
     */
    //export function groupBy<K, V>(list: Array<V>, keyGetter: (input: V) => K): Map<K, Array<V>> {
    //    const map = new Map<K, Array<V>>();
    const map = new Map();
    list.forEach((item) => {
         const key = keyGetter(item);
         const collection = map.get(key);
         if (!collection) {
             map.set(key, [item]);
         } else {
             collection.push(item);
         }
    });
    return map;
  }
  
  
  export function getRightSetDifferenceOfArrays(arr1, arr2){
    /*Get items in arr1 that are not in arr2
    */
    let difference = arr1.filter(x => !arr2.includes(x))
    return difference
  }
  
  export function getSetDifferenceOfArrays(arr1, arr2){
    /*Get symmetric difference between two arrays
    */
    let difference = arr1.filter(x => !arr2.includes(x)).concat(arr2.filter(x => !arr1.includes(x)))
    return difference
  }
  
    
  export function getFormattedMilliseconds(milliseconds){
      let formatted = ''
      if (milliseconds >= 60000){
        const intermediate = milliseconds / 60000 
        formatted = `${intermediate.toFixed(2)} min`
      } else if (milliseconds < 60000 && milliseconds >= 1000){
        const intermediate = milliseconds / 1000 
        formatted = `${intermediate.toFixed(2)} sec`
      } else {
        formatted = `${milliseconds.toFixed(2)} milliseconds`
      }
      return formatted
    }
    
    /* FAIL: this is too complicated, but may be something to consider in future
    export function getFileReferenceNumber(filename, searchTermOrIndexArray=/(^\d+)(.+$)/i, regex=true){
      /* Get a file reference number from file name
      This unique identifier is used throughout the app.  If no ref number is used, then a hash
      of the file name will be applied for uniqueness.
      ref: https://stackoverflow.com/questions/7616461/generate-a-hash-from-string-in-javascript
    
      The `searchTermOrIndexArray` argument should be one of the following:
       * Array [start, stop] - index numbers to slice
       * String (chars) - simple search term to slice(0, first_index)
       * String (regex) - regex pattern to hit
        
       ('54931863796627370000-econ_2301.00410.pdf').replace(regex, '$1')
       '54931863796627370000'
      *//*
     let reference = ''
     if (Array.isArray(searchTermOrIndexArray)==true && searchTermOrIndexArray.length==2){
      let idx1,idx2
      [idx1, idx2] = searchTermOrIndexArray
      let tmp = filename.slice(idx1, idx2)
      if (Number.isInteger(tmp)){
        reference = tmp
      } else {
        reference = filename.hashCode()
      }
     } else if (typeof(searchTermOrIndexArray)=="string"){
          if (!regex){
            const idx = filename.indexOf(searchTermOrIndexArray)
            reference = filename.slice(0, idx)
          } else if (regex){
            let tmp = (filename).replace(searchTermOrIndexArray, '$1')
            if (tmp.length <= 20 ){
              console.log(tmp)
              reference = tmp
            }
          }
     } else {
      const reference = filename.hashCode()
    }
    return reference
    }*/
    
    
    export function getFileReferenceNumber(filename){
      /* Get a file reference number from file name
      This unique identifier is used throughout the app.  If no ref number is used, then a hash
      of the file name will be applied for uniqueness.
      
       ('54931863796627370000-econ_2301.00410.pdf').replace(regex, '$1')
       '54931863796627370000'
      */
     let reference = ''
     const regex = /(^\d+)(.+$)/i
     const rslt = (filename).replace(regex, '$1')
     if (rslt.length <= 20 && (Number.parseInt(rslt)).toString().length == rslt.length){
      reference = rslt
     } else {
      reference = filename.hashCode()
     }
     return reference
    }
    
    
    String.prototype.hashCode = function(seed = 0) {
      // Generate hash from string
      //ref: https://stackoverflow.com/questions/7616461/generate-a-hash-from-string-in-javascript
      let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
      for(let i = 0, ch; i < this.length; i++) {
          ch = this.charCodeAt(i);
          h1 = Math.imul(h1 ^ ch, 2654435761);
          h2 = Math.imul(h2 ^ ch, 1597334677);
      }
      h1  = Math.imul(h1 ^ (h1 >>> 16), 2246822507);
      h1 ^= Math.imul(h2 ^ (h2 >>> 13), 3266489909);
      h2  = Math.imul(h2 ^ (h2 >>> 16), 2246822507);
      h2 ^= Math.imul(h1 ^ (h1 >>> 13), 3266489909);
    
      return 4294967296 * (2097151 & h2) + (h1 >>> 0);
    };
    
    
    export const getDateFromJsNumber = num => {
      // Integer to string date
      let result = ''
      if (typeof(num)=='number'){
          if (String(num).length > 10) {
              let dt = new Date(num)
              result = `${dt.getMonth()+1}/${dt.getDate()}/${dt.getFullYear()}`;
          }
      } else if (typeof(num)=='string' && num.length > 10) {
          const int = parseInt(num) 
          let dt = new Date(int)
          result = `${dt.getMonth()+1}/${dt.getDate()}/${dt.getFullYear()}`;
      } 
      return result;
    };
    
    
    export function getFormattedFileSize(numberOfBytes, format='both') {
      /* Approximate to the closest prefixed unit
      
      format = <decimal, unit, both>
      getFormattedFileSize(139070, 'decimal')  >>> "135.81"
      getFormattedFileSize(139070, 'unit')  >>> "135.81 KiB"
      getFormattedFileSize(139070, 'both')  >>> "135.81 KiB (139070 bytes)"
      */
      const units = [
          "B",
          "KiB",
          "MiB",
          "GiB",
          "TiB",
          "PiB",
          "EiB",
          "ZiB",
          "YiB",
      ];
      const exponent = Math.min(
          Math.floor(Math.log(numberOfBytes) / Math.log(1024)),
          units.length - 1
      );
      const approx = numberOfBytes / 1024 ** exponent;
      let output = ''
      if(format == 'both'){
        output = exponent === 0 ?
              `${numberOfBytes} bytes` :
              `${approx.toFixed(2)} ${
                    units[exponent]
                  } (${numberOfBytes} bytes)`
      }else if (format == 'unit'){
        output =
              exponent === 0 ?
              `${numberOfBytes} bytes` :
              `${approx.toFixed(2)} ${
                    units[exponent]}`
      }else if (format == 'decimal'){
        output =
        exponent === 0 ?
        `${numberOfBytes} bytes` :
        `${approx.toFixed(2)}`
      }
      return output
    }
    
    
    export function camelize(str) {
      //Turn any string into camelCase
      return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function(word, index) {
          return index === 0 ? word.toLowerCase() : word.toUpperCase();
      }).replace(/\s+/g, '');
    }  