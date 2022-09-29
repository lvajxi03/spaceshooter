package main

import (
	"github.com/hajimehoshi/ebiten/v2"
)

func main() {
	ebiten.SetWindowSize(ARENA_WIDTH, ARENA_HEIGHT)
	ebiten.SetWindowTitle(APPLICATION_TITLE)
	ebiten.SetWindowDecorated(false)
	ebiten.SetFullscreen(true)

	// Game entry point
	shooter := &SpaceShooter{}
	ebiten.RunGame(shooter)
}
