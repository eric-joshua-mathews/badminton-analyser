def guess_shot(shuttleLocation,playerLocation,Px,Sx):
    shots={
        ("player_front", "shuttle_front"): "net",
        ("player_front", "shuttle_mid"): "deep push",
        ("player_front", "shuttle_rear"): "lift",
        ("player_mid", "shuttle_front"): "soft block",
        ("player_mid", "shuttle_mid"): "drive",
        ("player_mid", "shuttle_rear"): "deep drive",
        ("player_rear", "shuttle_front"): "drop",
        ("player_rear", "shuttle_mid"): "smash",
        ("player_rear", "shuttle_rear"): "clear",
    }
    shot_type= shots.get((playerLocation, shuttleLocation), "illegal shot")
    #cross or straight +direction
    dx = Sx-Px
    direction = "straight"
    if abs(dx) > 100:
        if dx<0:
            direction = "cross (left) "
        else:
            direction = "cross (right) "
    return f"{direction}{shot_type}"