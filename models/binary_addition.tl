1, 0 : digit.
order i 16 : index.
order n 3 : number.

var d, e : digit.
var i, j, k : index.
var a, b, c : number.

let bit : number, index -> digit. 

either atomic (a), operation (a).

leftArg (a, b) -> arg (a, b).
rightArg (a, b) -> arg (a, b).

leftArg (a, b), atomic (a) -> False.
rightArg (a, b), atomic (a) -> False.

arg (a, b), arg (b, a) -> False.

leftArg (a, b), bit (b, i, d) -> leftOperand (a, i, d).
rightArg (a, b), bit (b, i, d) -> rightOperand (a, i, d).

atomic (a), leftOperand (a, i, d) -> False.
atomic (a), rightOperand (a, i, d) -> False.

leftOperand (a, i, 1), rightOperand (a, i, 0) -> carryBit (a, i.next, 0).
leftOperand (a, i, 0), rightOperand (a, i, 0) -> carryBit (a, i.next, 0).
leftOperand (a, i, 0), rightOperand (a, i, 1) -> carryBit (a, i.next, 0).
leftOperand (a, i, 1), rightOperand (a, i, 1) -> carryBit (a, i.next, 1).

leftOperand (a, i, 0), rightOperand (a, i, 0), carryBit (a, i, 0) -> bit (a, i, 0).
leftOperand (a, i, 0), rightOperand (a, i, 0), carryBit (a, i, 1) -> bit (a, i, 1).
leftOperand (a, i, 0), rightOperand (a, i, 1), carryBit (a, i, 0) -> bit (a, i, 1).
leftOperand (a, i, 0), rightOperand (a, i, 1), carryBit (a, i, 1) -> bit (a, i, 0).
leftOperand (a, i, 1), rightOperand (a, i, 0), carryBit (a, i, 0) -> bit (a, i, 1).
leftOperand (a, i, 1), rightOperand (a, i, 0), carryBit (a, i, 1) -> bit (a, i, 0).
leftOperand (a, i, 1), rightOperand (a, i, 1), carryBit (a, i, 0) -> bit (a, i, 0).
leftOperand (a, i, 1), rightOperand (a, i, 1), carryBit (a, i, 1) -> bit (a, i, 1).


