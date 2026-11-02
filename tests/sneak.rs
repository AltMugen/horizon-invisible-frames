#[path="../mixins/invisible_frames/sneak.rs"] mod sneak;
#[test]
fn acting_player_input_is_isolated_and_updates_without_a_movement_tick() {
 sneak::record(1,true);sneak::record(2,false);
 assert!(sneak::is_sneaking(Some(1)));assert!(!sneak::is_sneaking(Some(2)));
 sneak::record(1,false);sneak::record(2,true);
 assert!(!sneak::is_sneaking(Some(1)));assert!(sneak::is_sneaking(Some(2)));
 assert!(!sneak::is_sneaking(None));assert!(!sneak::is_sneaking(Some(3)));
}
