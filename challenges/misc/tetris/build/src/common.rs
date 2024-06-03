use bevy::prelude::*;

#[derive(Debug, Clone, Eq, PartialEq, Hash, States, Default)]
pub enum AppState {
    #[default]
    MainMenu,
    InGame,
    GameOver,
    GameWon,
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash, States, Default)]
pub enum GameState {
    Playing,
    Paused,
    Restarted,
    #[default]
    Quited,
}
