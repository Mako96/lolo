import { TestBed } from '@angular/core/testing';

import { LoloUserProviderService } from './lolo-user-provider.service';

describe('LoloUserProviderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: LoloUserProviderService = TestBed.get(LoloUserProviderService);
    expect(service).toBeTruthy();
  });
});
