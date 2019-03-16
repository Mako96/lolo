import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModePage } from './mode.page';

describe('ModePage', () => {
  let component: ModePage;
  let fixture: ComponentFixture<ModePage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModePage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
