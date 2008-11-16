(* Test the Buffer module. *)

let () =
  let buf = Buffer.create 100 in
  for i = 0 to 10 do
    Buffer.add_char buf 'a';
    Buffer.add_string buf "b";
    Buffer.add_char buf 'c'
  done;
  let str = Buffer.contents buf in
  Printf.printf "contents of buffer = %S\n%!" str
