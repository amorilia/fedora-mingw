(* Another float/int conversion problem or difference. *)

open Printf ;;

printf "%d\n" (int_of_float (62.05 *. 60.)) ;;
let s = 62.05 *. 60. ;;
printf "%d\n" (int_of_float s) ;;
