open Printf

let () =
  printf "reported os_type = %S\n" Sys.os_type;
  printf "filename concat a b = %S\n" (Filename.concat "a" "b");
  printf "-1 = %d\n" (-1)
