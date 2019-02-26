import { TestBed } from '@angular/core/testing';

import { LoloPreferencesProviderService } from './lolo-preferences-provider.service';

describe('LoloPreferencesProviderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: LoloPreferencesProviderService = TestBed.get(LoloPreferencesProviderService);
    expect(service).toBeTruthy();
  });
});
