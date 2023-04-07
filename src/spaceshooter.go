package main

import (
	"errors"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	// "github.com/lvajxi03/bdlist"
)

// SpaceShooter is a main game structure type.
type SpaceShooter struct {
}

// Update is called with every next frame.
//
// Loop ends when this func returns nil.
func (shooter *SpaceShooter) Update() error {
	if inpututil.IsKeyJustPressed(ebiten.KeyQ) {
		return errors.New("Quit")
	}
	return nil
}

// Draw prepares and updates application screen.
func (shooter *SpaceShooter) Draw(scree *ebiten.Image) {
}

// Layout returns canvas width and height
// (implements Game interface)
func (shooter *SpaceShooter) Layout(w, h int) (screenWidth, screenHeight int) {
	return ARENA_WIDTH, ARENA_HEIGHT
}
