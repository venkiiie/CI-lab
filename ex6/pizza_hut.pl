:- dynamic menu_item/2.

% ----------- Initial menu -----------
menu_item('Margherita', 300).
menu_item('Pepperoni', 400).
menu_item('Veggie', 350).
menu_item('BBQ Chicken', 450).
menu_item('Farmhouse', 420).
menu_item('Paneer Tikka', 430).
menu_item('Cheese Burst', 480).
menu_item('Garlic Bread', 160).
menu_item('Cheesy Dip', 40).
menu_item('Coke', 60).
menu_item('Brownie', 120).

% ----------- Entry point -----------
order :-
    nl, writeln('Welcome to Pizza Hut!'),
    show_menu,
    nl, writeln('Start ordering. (Type "done" to finish).'),
    order_items([], RawOrder),
    merge_order(RawOrder, Order), % Combine duplicate items
    display_bill(Order).

% ----------- Show menu -----------
show_menu :-
    nl, writeln('-------- MENU --------'),
    format('~w~t~25|~w~n', ['Item', 'Price']),
    writeln('--------------------------------'),
    forall(menu_item(Item, Price),
           format('~w~t~25|~d~n', [Item, Price])),
    writeln('--------------------------------').

% ----------- Find item case-insensitively -----------
find_item(InputStr, RealName, Price) :-
    string_lower(InputStr, LowerInput),
    menu_item(RealName, Price),
    atom_string(RealName, MenuNameStr),
    string_lower(MenuNameStr, LowerInput),
    !. % Stop searching once found

% ----------- Take orders cleanly -----------
order_items(Current, Final) :-
    write('Enter item name: '), flush_output,
    read_line_to_string(user_input, InputStr),
    normalize_space(string(CleanStr), InputStr),
    
    ( string_lower(CleanStr, "done") ->
        Final = Current
    ; CleanStr == "" -> % User just pressed Enter by mistake
        order_items(Current, Final)
    ; find_item(CleanStr, RealName, Price) ->
        write('Enter quantity: '), flush_output,
        read_line_to_string(user_input, QtyStr),
        ( number_string(Qty, QtyStr) ->
            append(Current, [order(RealName, Qty, Price)], New),
            order_items(New, Final)
        ; writeln('Invalid quantity, try again.'),
          order_items(Current, Final)
        )
    ; % Item not in KB -> Add it
        format('Item not found. Enter price for "~w": ', [CleanStr]), flush_output,
        read_line_to_string(user_input, PriceStr),
        ( number_string(UserPrice, PriceStr) ->
            atom_string(NewItemAtom, CleanStr),
            assertz(menu_item(NewItemAtom, UserPrice)),
            format('Added "~w" to menu.~n', [NewItemAtom]),
            write('Enter quantity: '), flush_output,
            read_line_to_string(user_input, QtyStr2),
            ( number_string(Qty2, QtyStr2) ->
                append(Current, [order(NewItemAtom, Qty2, UserPrice)], New2),
                order_items(New2, Final)
            ; writeln('Invalid quantity, skipping...'),
              order_items(Current, Final)
            )
        ; writeln('Invalid price, try again.'),
          order_items(Current, Final)
        )
    ).

% ----------- Merge duplicate items -----------
merge_order(Raw, Merged) :- merge_order_(Raw, [], Merged).

merge_order_([], Acc, Acc).
merge_order_([order(Item, Qty, Price)|T], Acc, Out) :-
    ( select(order(Item, OldQty, Price), Acc, AccRest) ->
        NewQty is OldQty + Qty,
        Acc2 = [order(Item, NewQty, Price)|AccRest]
    ; Acc2 = [order(Item, Qty, Price)|Acc]
    ),
    merge_order_(T, Acc2, Out).

% ----------- Display bill -----------
display_bill(OrderList) :-
    nl, writeln('-------- BILL --------'),
    format('~w~t~25|~w~t~35|~w~n', ['Item', 'Qty', 'Subtotal']),
    writeln('-------------------------------------------'),
    bill_total(OrderList, 0, GrandTotal),
    writeln('-------------------------------------------'),
    format('Grand Total: ~d~n', [GrandTotal]),
    writeln('Thank you for ordering!').

bill_total([], Total, Total).
bill_total([order(Item, Qty, Price)|T], Acc, Total) :-
    SubTotal is Qty * Price,
    format('~w~t~25|~d~t~35|~d~n', [Item, Qty, SubTotal]),
    Acc2 is Acc + SubTotal,
    bill_total(T, Acc2, Total).
