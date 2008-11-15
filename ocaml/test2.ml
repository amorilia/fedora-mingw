open Printf
open Unix

let () =
  printf "$HOME = %S\n%!"
    (try Unix.getenv "HOME" with Not_found -> "(none)");
  printf "gettimeofday = %f\n%!" (Unix.gettimeofday ())

