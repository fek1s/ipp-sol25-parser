class Main : Object {
    run [|
        a := self foo: 4. "a = instance 14"
        b := [ :x | _ := 42. ]. "b = instance Block"
        c := b value: 16. "c = instance 42"
        d := 'ahoj' print.] "d = instance 'ahoj' - print vrací self , viz Vestavěné třídy"

    foo: [ :x |
        "s proměnnou 'u' se nijak dál nepracuje , ale výsledek zaslání
        zprávy 'plus:' bude vrácen jako výsledek volání metody 'foo'"
    u := x plus: 10.
    ]   
}
