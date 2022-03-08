module.exports = () => {
    console.log('Some code')
    return console.log('Some code')
}

// For example in a module, export function
exports.displayFullName = () => console.log('Full name')
exports.displayNickName = () => console.log('Nick name')

// In another module use those export
const { fullName, nickName } = require('./loadData.js')