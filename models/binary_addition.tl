1, 0 : digit.

order i 8 : index.

order s 2 : sum.
order n 4 : sumee.

order s 2 : number.
order n 4 : number.

var d, e : digit.
var i, j, k : index.
var s : sum.
var t : sumee.

let bit : number, index -> digit. 

let leftArg : sum -> sumee.
let rightArg : sum -> sumee.

leftArg (s, t), bit (t, i, d) -> leftOperand (s, i, d).
rightArg (s, t), bit (t, i, d) -> rightOperand (s, i, d).

carryBit (s, i1, 0).

leftOperand (s, i, 1), rightOperand (s, i, 0) -> carryBit (s, i.next, 0).
leftOperand (s, i, 0), rightOperand (s, i, 0) -> carryBit (s, i.next, 0).
leftOperand (s, i, 0), rightOperand (s, i, 1) -> carryBit (s, i.next, 0).
leftOperand (s, i, 1), rightOperand (s, i, 1) -> carryBit (s, i.next, 1).

leftOperand (s, i, 0), rightOperand (s, i, 0), carryBit (s, i, 0) -> bit (s, i, 0).
leftOperand (s, i, 0), rightOperand (s, i, 0), carryBit (s, i, 1) -> bit (s, i, 1).
leftOperand (s, i, 0), rightOperand (s, i, 1), carryBit (s, i, 0) -> bit (s, i, 1).
leftOperand (s, i, 0), rightOperand (s, i, 1), carryBit (s, i, 1) -> bit (s, i, 0).
leftOperand (s, i, 1), rightOperand (s, i, 0), carryBit (s, i, 0) -> bit (s, i, 1).
leftOperand (s, i, 1), rightOperand (s, i, 0), carryBit (s, i, 1) -> bit (s, i, 0).
leftOperand (s, i, 1), rightOperand (s, i, 1), carryBit (s, i, 0) -> bit (s, i, 0).
leftOperand (s, i, 1), rightOperand (s, i, 1), carryBit (s, i, 1) -> bit (s, i, 1).

