functor TicTacToe(Settings : TTTCONSTS) : ESTGAME =
struct

exception Unimplemented

(* Make our sequences better! *)
structure Seq = BetterSeq(Seq)
open Seq

datatype player = Minnie | Maxie
datatype outcome = Winner of player
datatype status = Over of outcome | In_play

(* NONE means no entry yet, SOME(e) means a tile has entry e *)
exception IllegalMove
datatype entry = O | X
type tile = entry option
type board = tile seq seq
type state = board * player
type location = int * int
type move = entry * location

structure Est : EST = Estimate
type est = Est.est

(* The start state is an n x n board of tiles. *)
val start : state = (
   tabulate (fn col => (tabulate (fn i => NONE) Settings.board_size))
             Settings.board_size, Maxie)


(* Don't worry about this one *)
fun data_to_start_state _ = start

val move_eq = (op =)

(* Might be a useful function... *)
fun other_player (p : player) =
    case p of
      Maxie => Minnie
    | Minnie => Maxie

(* is_valid_move : state * move -> bool
 * REQUIRES: true
 * ENSURES: is_valid_move(s, m) takes in a state and move and
 *          returns true if the move can be made on the board
 *          given in state and false otherwise.
 *)
fun is_valid_move (s : state, m : move) : bool =
    let
      val (piece, (row, col)) = m
      val (b, player) = s
      val cur : entry option = nth col (nth row b)
    in
      case ((row >= Settings.board_size orelse
             col >= Settings.board_size orelse
             row < 0 orelse col < 0), cur) of
           (true, _) => false
        |  (   _, NONE) => true
        |  (   _,    _) => false
    end

(* make_move : state * move -> state
 * REQUIRES: assume is move is valid
 * ENSURES: make_move(s, m) takes a state and a move, returns the
 *          new state if the move is valid
 *)
fun make_move (s : state, m : move) =
       let
         val (piece, (row, col)) = m
         val (b, player) = s
         val row_seq = nth row b
       in
         case player of
           Minnie =>
           (update (b, row, (update(row_seq, col, SOME(piece)))), Maxie)
        |  Maxie  =>
           (update (b, row, (update(row_seq, col, SOME(piece)))), Minnie)
       end


(* moves: state -> move seq
 * REQUIRES: true
 * ENSURES: moves takes in a state and returns a sequence of possible moves
 *          for the current player
 *)
fun moves (s : state) : move seq =
  let
    val (b, player) = s
    val b_size = Settings.board_size
    val b_pieces = b_size * b_size
    val b' = flatten(b)
    val unfilter_moves : move seq =
      tabulate (fn i => (
       case (nth i b', player) of
         (NONE, Maxie)  => (O, (i div b_size, i mod b_size))
       | (NONE, Minnie) => (X, (i div b_size, i mod b_size))
       | (SOME(e), _)   => (X, (~1, ~1)))) b_pieces
  in
    filter (fn (e, (r, c)) => not (r = ~1 andalso c = ~1)) unfilter_moves
  end


(* status : state -> status
 * REUQIRES: the state is valid
 * ENSURES: status takes in a state and evaluate to In_play if the game
 *          can still be continued and Over(outcome) if the game is over
 *          with outcome outcome.
 *)
fun status (s as (b, p) : state) : status =
  let
    val l = length(b)
    val move_length = length(moves(s))
    val rows = tabulate(fn i => tabulate (fn j => (i, j)) l) l
    val cols = tabulate(fn j => tabulate (fn i => (i, j)) l) l
    val tlbr = tabulate(fn _ => tabulate (fn i => (i, i)) l) l
    val trbl = tabulate(fn _ => tabulate (fn i => (i, l - 1 - i)) l) l
    val master_list = append(rows, append(cols, append(tlbr, trbl)))
    fun get r c = nth c (nth r b)
    val ocheck = mapreduce (fn sub => mapreduce(fn (r, c)=>(get r c = SOME O))
                   true (fn (a, b) => a andalso b) sub) (* sub is in matser *)
                   false (fn (a, b) => a orelse b) master_list

    val xcheck = mapreduce (fn sub => mapreduce(fn (r, c)=>(get r c = SOME X))
                   true (fn (a, b) => a andalso b) sub) (* sub is in matser *)
                   false (fn (a, b) => a orelse b) master_list
  in
    case (ocheck, xcheck, move_length = 0) of
      ( true , _ , _ ) => Over(Winner(Maxie))
   |  ( _ , true , _ ) => Over(Winner(Minnie))
   |  ( _ , _ , true ) => Over(Winner(Minnie))
   |  ( _ , _ , _    ) => In_play
  end



fun player ((_, p) : state) : player = p

fun outcome_to_est (Winner(Maxie)) = Est.MaxieWins
  | outcome_to_est (Winner(Minnie)) = Est.MinnieWins

fun outcome_to_string (Winner(Maxie)) = "Maxie wins"
  | outcome_to_string (Winner(Minnie)) = "Minnie wins"

fun player_to_string (Maxie : player) : string = "Maxie"
  | player_to_string Minnie = "Minnie"

(* implement *)
(* estimate : state -> Est.est
 * REQUIRES: the state is valid
 * ENSURES: estimate takes in a state and returns an estimated score for a given
 *          state
 *)
fun estimate ((b, p) : state) =
  let
    (* taken from the previous function *)
    val l = length(b)
    val rows = tabulate(fn i => tabulate (fn j => (i, j)) l) l
    val cols = tabulate(fn j => tabulate (fn i => (i, j)) l) l
    val tlbr = tabulate(fn _ => tabulate (fn i => (i, i)) l) l
    val trbl = tabulate(fn _ => tabulate (fn i => (i, l - 1 - i)) l) l
    val master_list = append(rows, append(cols, append(tlbr, trbl)))
    fun get r c = nth c (nth r b)
    fun score sub main oppo =
      (* given a sequence of coordinates, we check if this given sequence
       * has any opponent's piece in it *)
      case (mapreduce (fn (r, c) => get r c = oppo)
            false (fn (x, y) => x orelse y) sub) of
      (* if it does, we know the main player cannot win on this sequence
       * because it has some opponent's piece on it *)
      true => 0
      (* if it doesn't, we find the number of my pieces
       * and return a positive value associated with that number *)
    | false => (mapreduce (fn (r, c) =>
                case (get r c = main) of
                  true => 1
                |false => 0) 0 (fn (x, y) => x + y) sub)
     (* we check each component in master_list the score corresponding to each
      * component and we return the sum of these scores for each player *)
     val score_x = mapreduce (fn sub_seq => score sub_seq (SOME X)(SOME O))
                   0 (fn (x, y) => x + y) master_list
     val score_o = mapreduce (fn sub_seq => score sub_seq (SOME O)(SOME X))
                   0 (fn (x, y) => x + y) master_list
   in
     case (status (b, p)) of
       Over(Winner(Maxie)) => Est.MaxieWins
    |  Over(Winner(Minnie)) => Est.MinnieWins
    |  In_play  => Est.Guess(score_o - score_x)
    (* score x is the points given to Maxie, and score_o is the points
     * given to Minnie. the difference between them tell us the estimated
     * value of the state, with higher value favoring Maxie and lower
     * value favoring Minnie *)
   end

(* The given functions below are for playing the game - no need to worry about these *)
(* That being said, DON'T CHANGE THEM *)
(* Colors for to_string methods *)
val color_O = Ansi.bright_cyan
val color_X = Ansi.bright_magenta

fun entry_to_string (O : entry) : string = Ansi.colorStr "O" {bg = NONE, fg = SOME(color_O)}
  | entry_to_string X = Ansi.colorStr "X" {bg = NONE, fg = SOME(color_X)}

fun detailed_move_to_string ((b,p) : state, (e,(r,c)) : move) =
    (player_to_string p) ^ " placed an " ^
    (entry_to_string e) ^ " onto row " ^
    Int.toString(r) ^ " and column " ^
    Int.toString(c)

fun move_to_string ((e, (r,c)) : move) : string =
    "Placed " ^ (entry_to_string e) ^
    " on location (" ^ Int.toString(r) ^ ", " ^ Int.toString(c) ^ ")"

val turn_color = Ansi.bright_yellow
fun state_to_string ((b, p) : state) =
    let
      val divider = String.concat (List.tabulate (4 * Settings.board_size + 1,(fn _ => "-")))
      fun eopt_to_string eo = case eo of
                                SOME(O) => " O "
                              | SOME(X) => " X "
                              | NONE => " - "
      fun row_to_string (s : entry option seq) =
          "|" ^ String.concatWith "|" (Seq.toList(Seq.map eopt_to_string s)) ^ "|"
      val rowStrings = Seq.map row_to_string b
      val boardString = String.concatWith ("\n" ^ divider ^ "\n") (Seq.toList rowStrings)
      val nextMoveString = Ansi.colorStr ((player_to_string p) ^ " to move. Board State:")
                                         {bg = NONE, fg = SOME(turn_color)}
    in
      nextMoveString ^ "\n\n" ^ divider ^ "\n" ^ boardString ^ "\n" ^ divider ^ "\n"
    end

(* Maintains the invariant as given in the signature *)
fun move_to_descriptor ((_,(r,c)) : move) = Int.toString(r) ^ " " ^ Int.toString(c)

fun parse_move ((b, p) : state) (str : string) : move option =
    let
      val tokens = String.tokens (fn x => x = #" ") str
    in
      case tokens of
        [r,c] => (case (Int.fromString(r), Int.fromString(c)) of
                    (SOME(row),SOME(col)) => if p = Maxie
                                             then SOME(O, (row, col))
                                             else SOME(X, (row, col))
                  | _ => NONE)
      | _ => NONE
    end

end

(* Test Cases *)
functor TestOne(T: ESTGAME) =
struct
  structure TT = T
  open TT
  val state0 : state = start

  val moves_seq = moves(state0)

  val move0 = Seq.nth 0 moves_seq
  val move1 = Seq.nth 1 moves_seq
  val move2 = Seq.nth 2 moves_seq
  val move3 = Seq.nth 3 moves_seq

  val true = is_valid_move(state0, move0)
  val true = is_valid_move(state0, move1)
  val true = is_valid_move(state0, move2)
  val true = is_valid_move(state0, move3)

  val move4 = let val SOME(x) = parse_move state0 "0 0" in x end
  val state1 = make_move(state0, move4)
  val false = is_valid_move(state1, move4)
  val 3 = Seq.length(moves(state1))
  val true = move_eq(move0, move4)
  val false = move_eq(move1, move4)

  val In_play = status(state0)
  val In_play = status(state1)

  val move5 = let val SOME(x) = parse_move state1 "0 1" in x end
  val state2 = make_move(state1, move5)
  val false = is_valid_move(state2, move5)
  val 2 = Seq.length(moves(state2))
  val In_play = status(state2)

  val move6 = let val SOME(x) = parse_move state2 "1 0" in x end
  val state3 = make_move(state2, move6)
  val false = is_valid_move(state3, move6)
  val 1 = Seq.length(moves(state3))
  val Over(Winner(Maxie)) = status(state3)
  val MaxieWins = estimate(state3)
  val Est.Guess(0) = estimate(state0)
  val Est.Guess(4) = estimate(state1)
  val Est.Guess(0) = estimate(state2)
end

structure TESTALL = TestOne(TicTacToe(struct val board_size = 2 end))





















