(* Look for assembler errors like this:
 * 'Warning: 9223372036854775807 shortened to 4294967295'
 * Try to reproduce and fix.
 *)

open Printf

let () =
  let i = max_int in			(* Different on 32 & 64 bit platforms.*)
  printf "max_int = %d\n" i;
  let i = min_int in
  printf "min_int = %d\n" i;
  let i64 = Int64.max_int in		(* Same on all platforms. *)
  printf "Int64.max_int = %Ld\n" i64;
  let i32 = Int32.max_int in
  printf "Int32.max_int = %ld\n" i32;

  (* This is how the stdlib computes min_int:
   *   min_int = 1 lsl (if 1 lsl 31 = 0 (* ie. 32 bit *) then 30 else 62)
   *)
  printf "1 lsl 31 = %d\n" (1 lsl 31);
  printf "1 lsl 30 = %d\n" (1 lsl 30);
  printf "1 lsl 62 = %d\n" (1 lsl 62)
