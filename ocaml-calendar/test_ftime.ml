(*i $Id: test_ftime.ml,v 1.2 2008/02/08 10:36:14 signoles Exp $ i*)

Printf.printf "Tests of Ftime:\n";;

open CalendarLib
open Ftime;;
include Gen_test;;
reset ();;

Time_Zone.change (Time_Zone.UTC_Plus 10);;

(* Some [=] are used which should be replaced by [equal]. *)

test (make 30 60 80.5 = make 31 1 20.5) "30-60-80.5 = 31-1-20.5";;
test (normalize (make 22 0 0.1) = (make 22 0 0.1, 0)) "normalize 22-0-0.1";;
test (normalize (make 73 0 0.) = (make 1 0 0., 3)) "normalize 73-0-0";;
test (normalize (make (-73) 0 0.) = (make 23 0 0., -4)) "normalize (-73)-0-0";;
test (add (make 20 0 0.2) (Period.minute 70) = make 21 10 0.2) 
  "add 20-0-0.2 70mn";;
test (next (make 20 3 31.) `Minute = make 20 4 31.) "next 20-3-31 `Minute";
test (prev (make 20 3 31.34) `Second = make 20 3 30.34) 
  "prev 20-3-31.34 `Second";;
test (Period.equal (sub (make 6 5 4.) (make 4 5 6.1)) (Period.make 1 59 57.9))
  "sub 6-5-4. 4-5-6.1";;
test (convert (make 20 0 0.123) (Time_Zone.UTC_Plus 2) (Time_Zone.UTC_Plus 4) = 
	make 22 0 0.123) "convert";;
test (to_gmt (make 20 0 0.) = make 10 0 0.) "to_gmt";;
test (from_gmt (make 20 0 0.) = make 30 0 0.) "from_gmt";;
test (midnight () = make 0 0 0.) "midnight";;
test (midday () = make 12 0 0.) "midday";;
test (hour (make 20 0 59.99) = 20) "hour";;
test (minute (make 20 10 0.) = 10) "minute";;
test (second (make 20 10 5.) = 5.) "second";;

let one_two_three = make 1 2 3.;;
test (to_seconds one_two_three = 3723.) "to_seconds";;
test (to_minutes one_two_three = 62.05) "to_minutes";;
test (Utils.Float.equal (to_hours (make 1 3 0.4)) 1.050111) "to_hours";;
test (equal (from_seconds 3723.2) (from_minutes 62.053333333)) 
  "from_seconds; from_minutes";;
test (from_hours 1.05 = make 1 3 0.) "from_hours";;
test (is_pm (midnight ())) "is_pm midnight";;
test (is_pm (make 10 0 0.)) "is_pm 10-0-0";;
test (is_pm (make 34 0 0.)) "is_pm 34-0-0";;
test (not (is_pm (make (- 10) 0 0.))) "not (is_pm (- 10) 0 0)";;
test (is_am (midday ())) "is_am midday";;
test (is_am (make 20 0 0.)) "is_am 20-0-0";;
test (is_am (make (- 34) 0 0.)) "is_am (- 34) 0 0";;
test (not (is_am (make 34 0 0.))) "not (is_pm 34 0 0)";;

let one_two_three = Period.make 1 2 3.;;
let eq f1 f2 = abs_float (f1 -. f2) < 1e-5;;
test (eq (Period.to_seconds one_two_three) 3723.) "Period.to_seconds";;
test (eq (Period.to_minutes one_two_three) 62.05) "Period.to_minutes";;
test (Utils.Float.equal (Period.to_hours (Period.make 1 3 0.1)) 1.050028) 
  "Period.to_hours";;

let ok = nb_ok ();;
let bug = nb_bug ();;
Printf.printf "tests ok : %d; tests ko : %d\n" ok bug;;
flush stdout;;
