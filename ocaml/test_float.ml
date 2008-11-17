(* Float test, part of calendar test which was failing. *)

open Printf

let x = 1 * 3600 + 2 * 60 + 3 ;;

printf "minutes = %g\n" (float x /. 60.) ;;

printf "minutes (immediate) = 62.05 is %b\n" ((float x /. 60.) = 62.05) ;;

let m = float x /. 60. ;;

printf "minutes (variable) = 62.05 is %b\n" (m = 62.05) ;;

